using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using uPLibrary.Networking.M2Mqtt;

namespace MqttShow
{
    #region MqttMessage Class
    /// <summary>
    /// Class to hold a Mqtt Message.
    /// </summary>
    class MqttMessage
    {
        #region Classs Variables
        private string m_topic;
        private string m_message;
        #endregion

        #region Constructor
        /// <summary>
        /// Constructor
        /// </summary>
        /// <param name="t"></param>
        /// <param name="m"></param>
        public MqttMessage(string t, string m)
        {
            m_topic = t;
            m_message = m;
        }
        #endregion

        #region Topic Properity
        /// <summary>
        /// The Topic
        /// </summary>
        public string Topic
        {
            get
            {
                return m_topic;
            }
        }
        #endregion

        #region Message Properity
        /// <summary>
        /// The Message
        /// </summary>
        public string Message
        {
            get
            {
                return m_message;
            }
        }
        #endregion

        #region Payload Properity
        /// <summary>
        /// Return the message as a byte array, suitable as a payload.
        /// </summary>
        public byte[] Payload
        {
            get
            {
                return Encoding.ASCII.GetBytes(m_message);
            }
        }
        #endregion
    }
    #endregion

    class Mqtt
    {
        #region Class Variables...
        private List<MqttMessage> m_InputMessages;
        private List<MqttMessage> m_OutputMessages;
        private Thread m_MqttThread;
        private string m_Host;
        private int m_Port;
        private MqttClient m_client = null;
        private int m_nFailedToConnect = 0;
        private int m_nConnectionAttempts = 0;
        private int m_nConnectionClosed = 0;
        private int m_nExceptions = 0;
        private string m_ClientName;
        private object m_LockInputList = new object();
        private object m_LockOutputList = new object();
        private object m_ClientLock = new object();
        private AutoResetEvent m_eventNewMsgPending = new AutoResetEvent(false);
        private AutoResetEvent m_eventConnectionClosed = new AutoResetEvent(false);
        private long m_PingStartTime = 0;
        private bool m_kill = false;
        #endregion

        #region Events...
        /// <summary>
        /// Raised when a new message is added to the input queue...
        /// </summary>
        public event EventHandler NewMessageReady;
        /// <summary>
        /// Raised when the connection status has changed.
        /// </summary>
        public event EventHandler ConnectionStatusChanged;
        #endregion

        #region Event Triggers...
        private void TriggerNewMessage()
        {
            if (NewMessageReady != null)
            {
                NewMessageReady(this, new EventArgs());
            }
        }
        private void TriggerConnectionStatusChanged()
        {
            if (ConnectionStatusChanged != null)
            {
                ConnectionStatusChanged(this, new EventArgs());
            }
        }
        #endregion

        #region Construction
        /// <summary>
        /// Construction...
        /// </summary>
        /// <param name="Host"></param>
        /// <param name="Port"></param>
        /// <param name="ClientName"></param>
        public Mqtt(string Host, int Port, string ClientName)
        {
            m_Host = Host;
            m_Port = Port;
            m_ClientName = ClientName;
            m_InputMessages = new List<MqttMessage>();
            m_OutputMessages = new List<MqttMessage>();
            m_MqttThread = new Thread(new ThreadStart(RunInBackground));
            m_MqttThread.Name = "MqttMonitor";
            //m_MqttThread.Start();
        }
        #endregion

        #region Start()
        /// <summary>
        /// Starts the background MQTT Monitor
        /// </summary>
        public void Start()
        {
            if (m_MqttThread.IsAlive) return;
            m_MqttThread.Start();
        }
        #endregion

        #region Kill()
        /// <summary>
        /// Kill the MQTT client. 
        /// </summary>
        public void Kill()
        {
            m_kill = true;
            if(m_MqttThread != null)
            {
                m_MqttThread.Abort();
            }
        }
        #endregion

        #region IsConnected Property
        /// <summary>
        /// True if connected.
        /// </summary>
        public bool IsConnected
        {
            get
            {
                bool IsConnected = false;
                lock(m_ClientLock)
                {
                    if (m_client != null && m_client.IsConnected) IsConnected = true;
                }
                return IsConnected;
            }
        }
        #endregion

        #region SendMessage()
        /// <summary>
        /// Puts a message in the queue for sending. 
        /// </summary>
        /// <param name="topic">Message topic.</param>
        /// <param name="msg">Message Content</param>
        public void SendMessage(string topic, string msg)
        {
            MqttMessage m = new MqttMessage(topic, msg);
            lock (m_LockOutputList)
            {
                m_OutputMessages.Add(m);
            }
            m_eventNewMsgPending.Set();
        }
        #endregion

        #region GetMessages()
        /// <summary>
        /// Reterive all messages since last call.
        /// </summary>
        public MqttMessage[] GetMessages()
        {
            MqttMessage[] m_Msgs;
            lock(m_LockInputList)
            {
                m_Msgs = m_InputMessages.ToArray();
                m_InputMessages.Clear();
            }
            return m_Msgs;
        }
        #endregion

        #region TryToConnect()
        /// <summary>
        /// Try to stay connected to the broker at all times.
        /// </summary>
        private bool TryToConnect()
        {
            try
            {
                MqttClient tempclient;
                lock (m_ClientLock)
                {
                    tempclient = m_client;
                }
                if (tempclient != null && tempclient.IsConnected) return true;
                tempclient = new MqttClient(m_Host, m_Port, false, MqttSslProtocols.None, null, null);
                String[] topics = new string[1];
                byte[] qoslevels = new byte[1];
                topics[0] = "robot/#";
                qoslevels[0] = 0;
                tempclient.MqttMsgPublishReceived += RawMsgReceived;
                tempclient.ConnectionClosed += ConnectionClosed;
                tempclient.Subscribe(topics, qoslevels);
                tempclient.Connect(m_ClientName, null, null, false, 0, false, "", "", true, 10);
                //m_client.Connect(m_ClientName);
                lock (m_ClientLock)
                {
                    m_client = tempclient;
                }
                return true;
            }
            catch (uPLibrary.Networking.M2Mqtt.Exceptions.MqttConnectionException ee)
            {
                //Console.Write("Exeption Caught while trying to connect.");
                m_nFailedToConnect++;
                lock (m_ClientLock)
                {
                    m_client = null;
                }
                return false;
            }
        }
        #endregion

        #region ConnectionClosed()
        /// <summary>
        /// Callback when the connection is closed.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void ConnectionClosed(object sender, EventArgs e)
        {
            Console.Write("\nIn Connection Closed...\n");
            lock (m_ClientLock)
            {
                m_client = null;
            }
            m_eventConnectionClosed.Set();
        }
        #endregion

        #region RawMsgReceived()
        /// <summary>
        /// Callback for when a message comes in.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void RawMsgReceived(object sender, uPLibrary.Networking.M2Mqtt.Messages.MqttMsgPublishEventArgs e)
        {
            // A new message has come it.  Put it in our list.
            string payload = System.Text.Encoding.ASCII.GetString(e.Message);
            MqttMessage m = new MqttMessage(e.Topic, payload);
            if(e.Topic == "robot/jetson/ping")
            {
                double ElapsedSecs = StopWatch.Stop(m_PingStartTime);
                Console.Write(String.Format("\nPing = {0:000.00000}\n\n", ElapsedSecs * 1000.0));
            }

            lock(m_LockInputList)
            {
                m_InputMessages.Add(m);
            }
            TriggerNewMessage();
        }
        #endregion

        #region SendRawMessages()
        /// <summary>
        /// Send the pending messages on the background thread.
        /// </summary>
        private bool SendRawMessages()
        {
            MqttMessage[] msgs;
            lock(m_LockOutputList)
            {
                msgs = m_OutputMessages.ToArray();
                m_OutputMessages.Clear();
            }

            foreach (MqttMessage m in msgs)
            {
                MqttClient tempclient;
                lock (m_ClientLock)
                {
                    tempclient = m_client;
                }
                if (tempclient == null) return false;
                if (!tempclient.IsConnected) return false;
                try
                {
                    if (m.Topic == "robot/pingtest") m_PingStartTime = StopWatch.Start();
                    m_client.Publish(m.Topic, m.Payload);
                }
                catch (Exception ee)
                {
                    Console.Write("Error trying to send message. E= " + ee.Message);
                    return false;
                 }
            }
            return true;
        }
        #endregion

        #region RunInBackground()
        /// <summary>
        /// Background Monitor and Runing of our loop.
        /// </summary>
        private void RunInBackground()
        {
            while (true)   
            {
                while (true)
                {
                    m_nConnectionAttempts++;
                    Console.Write("\nCalling StayConnected...\n");
                    bool okay = TryToConnect();
                    if (okay) break;
                    Thread.Sleep(200);
                }
                Console.Write("We are connected. on Thread " + Thread.CurrentThread.Name);
                // Loop here to send messages or until something goes wrong...
                bool bGoodToRun = true;
                while (bGoodToRun)
                {
                    WaitHandle[] items = new WaitHandle[2];
                    items[0] = m_eventNewMsgPending;
                    items[1] = m_eventConnectionClosed;
                    int isignal = WaitHandle.WaitAny(items);

                    switch (isignal)
                    {
                        case 0:
                            bool okay = SendRawMessages();
                            if (!okay) bGoodToRun = false;
                            break;
                        case 1:
                            Console.Write("Connection Failure.  Retrying.");
                            bGoodToRun = false;
                            break;
                        default:
                            Console.Write("Weird value from WantAny!!!");
                            bGoodToRun = false;
                            break;
                    }
                }
                // If we fall out of the while loop, that can only happen because
                // an error or we lost connection.  So start over.
                lock (m_ClientLock)
                {
                    m_client = null;
                }
                TriggerConnectionStatusChanged();
                Thread.Sleep(200);  // Wait a little while here to let things settle down.
                if (m_kill) break;
            }
        }
        #endregion
    }
}
