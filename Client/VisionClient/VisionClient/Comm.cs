// --------------------------------------------------------------------
// Comm.cs -- network communications
//
// Created 3/01/17 DLB, TastyDucks
// --------------------------------------------------------------------

using System;
using System.IO;
using System.Net.Sockets;
using System.Threading;

namespace VisionClient
{
    #region Comm class
    /// <summary>
    /// Comm Class to establish comm with Jetson
    /// </summary>
    public class Comm
    {
        #region Events...
        /// <summary>
        /// Fired on comm thread when data is ready.
        /// </summary>
        public event EventHandler DataReady;
        public event EventHandler StatusChanged;
        #endregion

        #region Class Variables...
        TcpClient m_Client = null;
        string m_ServerIP = "10.44.15.19";
        int m_ServerPort = 5800;
        bool m_IsRunning = false;
        bool m_AbortComm = false;
        bool m_RestartComm = false;
        string m_SendData = "";
        bool m_SendDataEmpty = true;
        ManualResetEvent m_KillAll = new ManualResetEvent(false);
        ManualResetEvent m_ComFail = new ManualResetEvent(false);
        ManualResetEvent m_SenderDone = new ManualResetEvent(false);
        ManualResetEvent m_ReceiverDone = new ManualResetEvent(false);
        ManualResetEvent m_ManagerDone = new ManualResetEvent(false);
        AutoResetEvent m_SendDataReady = new AutoResetEvent(false);
        object m_OutputLock = new object();
        byte[] m_OutputData = null;
        bool m_OutputReady = false;
        #endregion

        #region TriggerDataReady()
        private void TriggerDataReady()
        {
            EventArgs e = new EventArgs();
            if (DataReady != null)
                DataReady(this, e);
        }
        #endregion

        #region TriggeStatusChanged()
        private void TriggeStatusChanged()
        {
            EventArgs e = new EventArgs();
            if (StatusChanged != null)
                StatusChanged(this, e);
        }
        #endregion 

        #region SetAddress()
        /// <summary>
        /// Sets the address and port to the Jetson where we will receive data.  Must be 
        /// called before calling Run(), or at least while communications are stopped.
        /// </summary>
        /// <param name="IP"></param>
        /// <param name="port"></param>
        public void SetAddress(string IP, int port)
        {
            m_ServerIP = IP;
            m_ServerPort = port;
        }
        #endregion

        #region Run()
        /// <summary>
        /// Starts the communications.  Should be called once.  This will start a
        /// separate thread that does all communications.
        /// </summary>
        public void Run()
        {
            if (m_IsRunning) return;
            m_IsRunning = true;
            m_RestartComm = false;
            m_AbortComm = false;
            m_SenderDone.Reset();
            m_ReceiverDone.Reset();
            m_ManagerDone.Reset();
            Thread m_CommThread = new Thread(new ThreadStart(this.ManageComm));
            m_CommThread.IsBackground = true;
            m_CommThread.Start();
        }
        #endregion

        #region Stop()
        /// <summary>
        /// Stops the communication.  Used to change IP address and then call Run() again.
        /// </summary>
        public void Stop()
        {
            if (!m_IsRunning) return;
            m_AbortComm = true;
            m_KillAll.Set();
            m_ManagerDone.WaitOne();
            m_IsRunning = false;
            m_AbortComm = false;
        }
        #endregion

        #region IsCommected()
        /// <summary>
        /// Returns a bool indicating if we are connected to the Jetson.
        /// </summary>
        /// <returns></returns>
        public bool IsConnected()
        {
            if (!m_IsRunning) return false;
            if (m_Client == null) return false;
            return m_Client.Connected;
        }
        #endregion

        #region SendData()
        /// <summary>
        /// Sends data to the Jetson.  Returns true if no obvious errors
        /// where detected, otherwise false is returned of there is 
        /// no connection, or if the previous data has not been sent.  Note:
        /// there is no garuntee that the data will be received.
        /// </summary>
        /// <param name="Message"></param>
        /// <returns></returns>
        public bool SendData(string Message)
        {
            if(!m_IsRunning || !m_SendDataEmpty)
            {
                return false;
            }
            m_SendDataEmpty = false;
            m_SendData = Message;
            m_SendDataReady.Set();
            return true;
        }
        #endregion

        #region ManageSend()
        /// <summary>
        /// Manage the sending of data while also monitoring for com failure, or outright abort.
        /// </summary>
        private void ManageSend()
        {
            while (true)
            {
                if (m_Client == null || !m_Client.Connected)
                {
                    m_SendDataEmpty = true;
                    m_ComFail.Set();
                    m_SenderDone.Set();
                    return;
                }
                WaitHandle[] evnts = new WaitHandle[3];
                evnts[0] = m_KillAll;
                evnts[1] = m_ComFail;
                evnts[2] = m_SendDataReady;
                int irst = WaitHandle.WaitAny(evnts);
                if (irst != 2)
                {
                    m_SendDataEmpty = true;
                    m_ComFail.Set();
                    m_SenderDone.Set();
                    return;
                }
                NetworkStream Stream = m_Client.GetStream();
                System.Text.ASCIIEncoding asen = new System.Text.ASCIIEncoding();
                byte[] ba = asen.GetBytes(m_SendData);
                try
                {
                    Stream.Write(ba, 0, ba.Length);
                    m_SendDataEmpty = true;
                }
                catch (System.IO.IOException e)
                {
                    m_SendDataEmpty = true;
                    m_ComFail.Set();
                    m_SenderDone.Set();
                    return;
                }
            }
        }
        #endregion

        #region GetData()
        /// <summary>
        /// Gets data that has been received.  If no new data to get, null is
        /// returned.
        /// </summary>
        /// <returns></returns>
        public byte[] GetData()
        {
            byte[] data = null;
            lock(m_OutputLock)
            {
                if (m_OutputReady)
                {
                    data = new byte[m_OutputData.Length];
                    Array.Copy(m_OutputData, data, data.Length);
                    m_OutputReady = false;
                }
            }
            return data;
        }
        #endregion

        #region ManageReceive()
        /// <summary>
        /// Manage the receiving of data while also monitoring for com failure, or outright abort.
        /// </summary>
        private void ManageReceive()
        {
            while (true)
            {
                if (m_Client == null || !m_Client.Connected)
                {
                    m_ComFail.Set();
                    m_ReceiverDone.Set();
                    return;
                }
                NetworkStream strm = m_Client.GetStream();
                StreamReader reader = new StreamReader(strm);
                string InputData;
                try
                {
                    while (true)
                    {
                        InputData = reader.ReadLine();
                        if (InputData != null) break;
                    }
                }
                catch (System.IO.IOException e)
                {
                    m_ComFail.Set();
                    m_ReceiverDone.Set();
                    return;
                }
                lock (m_OutputLock)
                {
                    m_OutputData = Convert.FromBase64String(InputData);
                    m_OutputReady = true;
                }
                TriggerDataReady();
                WaitHandle[] evnts = new WaitHandle[2];
                evnts[0] = m_KillAll;
                evnts[1] = m_ComFail;
                int indx = WaitHandle.WaitAny(evnts, 2);
                if (indx == 0 || indx == 1)
                {
                    m_ComFail.Set();
                    m_ReceiverDone.Set();
                    return;
                }
            }
        }
        #endregion

        #region ConnectRaw()
        /// <summary>
        /// Trys to connect to the Jetson with the given timeout. Returns true if
        /// a connection is successful, false otherwise.
        /// </summary>
        /// <param name="timeout"></param>
        /// <returns></returns>
        private bool ConnectRaw(TimeSpan timeout)
        {
            try
            {
                m_Client = new TcpClient();
                m_Client.ReceiveBufferSize = 300000;
                var result = m_Client.BeginConnect(m_ServerIP, m_ServerPort, null, null);
                var success = result.AsyncWaitHandle.WaitOne(timeout);
                if (!success)
                {
                    m_Client.Close();
                    m_Client = null;
                    return false;
                }
                // we have connected
                m_Client.EndConnect(result);
                return true;
            }
            catch (System.Net.Sockets.SocketException e)
            {
                Thread.Sleep(200);
                return false;
            }
        }
        #endregion

        #region ManageComm()
        /// <summary>
        /// ManageComm runs on a background thread and does all communications.
        /// </summary>
        private void ManageComm()
        {
            while (true)
            {
                m_RestartComm = false;
                m_SenderDone.Reset();
                m_ReceiverDone.Reset();
                m_ComFail.Reset();
                while (true)
                {
                    bool okay = ConnectRaw(TimeSpan.FromSeconds(2.0));
                    if (okay) break;
                    if (m_AbortComm)
                    {
                        m_IsRunning = false;
                        return;
                    }
                }
                // At this point we should be connected.
                TriggeStatusChanged();
                // Start the sending and receiving threads.  Wait for a problem.
                Thread sender = new Thread(new ThreadStart(this.ManageSend));
                Thread receiver = new Thread(new ThreadStart(this.ManageReceive));
                sender.IsBackground = true;
                sender.Start();
                receiver.IsBackground = true;
                receiver.Start();
                // Now wait until there is a problem, or we are called upon to exit.
                WaitHandle[] evnts = new WaitHandle[2];
                evnts[0] = m_SenderDone;
                evnts[1] = m_ReceiverDone;
                WaitHandle.WaitAll(evnts);
                TriggeStatusChanged();
                if (m_AbortComm)
                {
                    m_ManagerDone.Set();
                    break;
                }
            }
        }
        #endregion
    }
    #endregion
}
