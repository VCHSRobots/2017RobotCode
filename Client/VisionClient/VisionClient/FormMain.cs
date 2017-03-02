using System;
using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Net.Sockets;
using System.Threading;
using System.Windows.Forms;

namespace VisionClient
{
    public partial class FormMain : Form
    {
        #region Class Variables
        private delegate void VoidFunc();
        private delegate void EventFunc(object sender, EventArgs e);
        Comm m_Comm = null;
        //TcpClient Client = new TcpClient();
        //bool IsOnline = false;
        //string ServerIP = Properties.Settings.Default.IP;
        #endregion

        #region FormMain()
        public FormMain()
        {
            InitializeComponent();
            Log("VisionClient started!");
            m_Comm = new Comm();
            m_Comm.StatusChanged += CommStatusChange;
            m_Comm.DataReady += CommDataReady;
            m_Comm.SetAddress("10.44.15.19", 5800);
            m_Comm.Run();
            SetConnectionStatusUI();
            labelErrorInfo.Text = "";
        }
        #endregion

        protected override void OnResize(EventArgs e)
        {
            base.OnResize(e);
        }

        protected override void OnClosing(CancelEventArgs e)
        {
            base.OnClosing(e);
        }

        #region CommDataReady()
        /// <summary>
        /// This is called by the Comm object when a new picture is ready.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void CommDataReady(object sender, EventArgs e)
        {
            // This is probably called from a non-UI thread!  Do an invoke.
            if (this.InvokeRequired)
            {
                object[] args = new object[2];
                args[0] = sender;
                args[1] = e;
                this.Invoke(new EventFunc(CommDataReady), args);
                return;
            }
            byte[] data = m_Comm.GetData();
            labelErrorInfo.Text = "";
            try
            {
                using (MemoryStream ms = new MemoryStream(data))
                {
                    PictureBox.Image = Image.FromStream(ms);
                }
            }
            catch (Exception ee)
            {
                labelErrorInfo.Text = "Pic Conversion error: " + ee.ToString();
            }
        }
        #endregion

        #region SetConnectionStatusUI()
        /// <summary>
        /// Sets the flag on the UI for connection status.
        /// </summary>
        private void SetConnectionStatusUI()
        {
            if (this.InvokeRequired)
            {
                this.Invoke(new VoidFunc(SetConnectionStatusUI));
                return;
            }
            bool bConnected = m_Comm.IsConnected();
            if (bConnected)
            {
                this.labelConnectionStatus.Text = "Connected";
                this.labelConnectionStatus.ForeColor = Color.Green;
            }
            else
            {
                this.labelConnectionStatus.Text = "OFF LINE";
                this.labelConnectionStatus.ForeColor = Color.Red;
            }
        }
        #endregion

        #region CommStatusChange()
        /// <summary>
        /// This is called by the Comm object when the connection status changes.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void CommStatusChange(object sender, EventArgs e)
        {
            // This is probably called from a non-UI thread!  Do an invoke in the target!
            SetConnectionStatusUI();
        }
        #endregion

        #region //Networking and Communications
        //private void ConnectionTimer_Tick(object sender, EventArgs e)
        //{
        //    if (IsOnline == true)
        //    {
        //        Send("1");
        //        LabelStatus.Text = "Current connection status: ONLINE.";
        //    }
        //    else
        //    {
        //        Connect();
        //    }
        //}
        //private void Connect()
        //{
        //    Log("Attempting to connect to server at \"" + ServerIP + ":5800\"...");
        //    try
        //    {
        //        Client.Connect(ServerIP, 5800);
        //        Send("C");
        //        System.Threading.Thread.Sleep(1000);
        //        Send("T");
        //        LabelStatus.Text = "Current connection status: ONLINE.";
        //        IsOnline = true;
        //    }
        //    catch (Exception e)
        //    {
        //        LabelStatus.Text = "Current connection status: OFFLINE.";
        //        IsOnline = false;
        //        Log("Failed to connect to server:\r\n" + e);
        //    }
        //}
        //private void Listen()
        //{
        //    while (true)
        //    { 
        //        try
        //        {
        //            NetworkStream strm = Client.GetStream();
        //            StreamReader reader = new StreamReader(strm);
        //            string line = reader.ReadLine();
        //            byte[] pic = Convert.FromBase64String(line);
        //            using (MemoryStream ms = new MemoryStream(pic))
        //            {
        //                PictureBox.Image = Image.FromStream(ms);
        //            }
        //        }
        //        catch
        //        {
        //            continue;
        //        }
        //    }
        //}
        //private void Send(string Message)
        //{
        //    Log("Attempting to send data...");
        //    try
        //    {
        //        NetworkStream Stream = Client.GetStream();
        //        System.Text.ASCIIEncoding asen = new System.Text.ASCIIEncoding();
        //        byte[] ba = asen.GetBytes(Message);
        //        Stream.WriteAsync(ba, 0, ba.Length);
        //        IsOnline = true;
        //        LabelStatus.Text = "Current connection status: ONLINE.";
        //        Log("Data sent to server: " + Message);
                
        //    }
        //    catch (Exception e)
        //    {
        //        IsOnline = false;
        //        LabelStatus.Text = "Current connection status: OFFLINE.";
        //        Log("ERROR: Failed to send data to server: client offline:\r\n" + e);
        //    }
        //}
        //private void RefreshTimer_Tick(object sender, EventArgs e)
        //{
        //    if (IsOnline == false)
        //    {
        //        LabelStatus.Text = "Current connection status: OFFLINE.";
        //    }
        //    if (IsOnline == true)
        //    {
        //        LabelStatus.Text = "Current connection status: ONLINE.";
        //    }
        //}
        #endregion

        #region FormMain_Shown()
        private void FormMain_Shown(object sender, EventArgs e)
        {
            //Connect();
            //ConnectionTimer.Start();
            //RefreshTimer.Start();
            //Client.ReceiveBufferSize = 300000;
            //Thread ListenThread = new Thread(Listen);
            //ListenThread.IsBackground = true;
            //ListenThread.Start();
            //ServerIP = Properties.Settings.Default.IP;
            //TextBoxIP.Text = ServerIP;
        }
        #endregion

        #region FormMain_FormClosed()
        private void FormMain_FormClosed(object sender, FormClosedEventArgs e)
        {
            Log("Shutting down VisionSystem...");
            m_Comm.Stop();
            Properties.Settings.Default.Save();
        }
        #endregion

        #region Log()
        private void Log(string message)
        {
            TextBoxTerminal.AppendText(message + "\r\n");
            File.WriteAllText("outlog.txt", message + "\r\n");
        }
        #endregion

        #region UI Events (Camera and Targeting Buttons)

        private void ButtonC0_Click(object sender, EventArgs e)
        {
            LabelCamera.Text = "Current camera: None";
            PictureBox.Image = Properties.Resources.C0;
            m_Comm.SendData("C0");
        }

        private void ButtonC1_Click(object sender, EventArgs e)
        {
            if(m_Comm.IsConnected())
            {
                m_Comm.SendData("C1");
                LabelCamera.Text = "Current camera: 1 / Front: Shooter";
            }
            else
            {
                LabelCamera.Text = "Current camera: None";
                PictureBox.Image = Properties.Resources.C0;
            }
        }
        private void ButtonC2_Click(object sender, EventArgs e)
        {
            if (m_Comm.IsConnected())
            {
                LabelCamera.Text = "Current camera: 2 / Front: General";
                m_Comm.SendData("C2");
            }
            else
            {
                LabelCamera.Text = "Current camera: None";
                PictureBox.Image = Properties.Resources.C0;
            }
        }
        private void ButtonC3_Click(object sender, EventArgs e)
        {
            if (m_Comm.IsConnected())
            {
                LabelCamera.Text = "Current camera: 3 / Front: Gear delivery";
                m_Comm.SendData("C3");
            }
            else
            {
                LabelCamera.Text = "Current camera: None";
                PictureBox.Image = Properties.Resources.C0;
            }
        }
        private void ButtonC4_Click(object sender, EventArgs e)
        {
            if (m_Comm.IsConnected())
            {
                LabelCamera.Text = "Current camera: 4 / Front: Rope climber";
                m_Comm.SendData("C4");
            }
            else
            {
                LabelCamera.Text = "Current camera: None";
                PictureBox.Image = Properties.Resources.C0;
            }
        }

        private void ButtonAimStop_Click(object sender, EventArgs e)
        {
            if (m_Comm.IsConnected())
                {
                m_Comm.SendData("T0");
            }
        }

        private void ButtonAimPeg_Click(object sender, EventArgs e)
        {
            if (m_Comm.IsConnected())
                {
                m_Comm.SendData("T2");
            }
        }

        private void ButtonAimBoiler_Click(object sender, EventArgs e)
        {
            if (m_Comm.IsConnected())
            {
                m_Comm.SendData("T1");
            }
        }
        #endregion

        #region UI Events (TabPageTerminal)

        private void TabControl_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (TabControl.SelectedTab == TabPageTerminal)
            {
                TextBoxTerminalInput.Focus();
            }
        }

        private void TextBoxTerminal_Enter(object sender, EventArgs e)
        {
            TextBoxTerminalInput.Focus();
        }

        private void TextBoxTerminalInput_KeyDown(object sender, KeyEventArgs e)
        {
            string RawInput = "";
            string Input = "";
            if (e.KeyCode == Keys.Enter)
            {
                TextBoxTerminal.AppendText("> " + TextBoxTerminalInput.Text + "\r\n");
                RawInput = TextBoxTerminalInput.Text;
                Input = RawInput.Trim().ToLower();
                TextBoxTerminalInput.Text = "";
                if (Input == "help" | Input == "?")
                {
                    TextBoxTerminal.AppendText("╔════════════════════════════╗\r\n║ VisionClient Terminal Help ║\r\n╚════════════════════════════╝\r\n\r\nCommands:\r\n\r\nclear\t\tClear the display.\r\nconnect\t\tAttempt to connect to the server, or ping the server if already connected.\r\ndisconnect\tDisconnect from the server.\r\nexit\t\tClose the VisionClient program. (Synonyms: \"bye\", \"quit\")\r\nhelp\t\tDisplay this menu. (Synonyms: \"?\")\r\nmagic\t\tAbracadabra!\r\nsend\t\tAttempt to send the entered data to the server. Syntax is: \"send <data>\". The server will listen for the following strings: \"C\", \"C0\", \"C1\", \"C2\", \"C3\", \"C4\", \"T\", \"T0\", \"T1\", \"T2\".\r\n");
                }
                else if (Input == "magic")
                {
                    TextBoxTerminal.AppendText(" ██████╗ ██╗  ██╗███████╗███████╗██████╗ ███████╗███████╗ █████╗ ██████╗ ███████╗\r\n██╔═████╗╚██╗██╔╝██╔════╝██╔════╝╚════██╗╚════██║██╔════╝██╔══██╗██╔══██╗██╔════╝\r\n██║██╔██║ ╚███╔╝ ███████╗█████╗   █████╔╝    ██╔╝███████╗╚██████║██║  ██║█████╗  \r\n████╔╝██║ ██╔██╗ ╚════██║██╔══╝   ╚═══██╗   ██╔╝ ╚════██║ ╚═══██║██║  ██║██╔══╝  \r\n╚██████╔╝██╔╝ ██╗███████║██║     ██████╔╝   ██║  ███████║ █████╔╝██████╔╝██║     \r\n ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═════╝    ╚═╝  ╚══════╝ ╚════╝ ╚═════╝ ╚═╝\r\n");
                }
                else if (Input == "clear")
                {
                    TextBoxTerminal.Text = "";
                }
                else if (Input == "connect")
                {
                    if (m_Comm.IsConnected())
                    {
                        m_Comm.SendData("1");
                        LabelStatus.Text = "Current connection status: ONLINE.";
                    }
                    else
                    {
                        m_Comm.Run();
                    }
                }
                else if (Input == "disconnect")
                {
                    m_Comm.Stop();
                    TextBoxTerminal.AppendText("Disconnected. Please note that you will not be able to reconnect for several minutes, due to underlying networking protocols.\r\n");
                }
                else if (Input == "quit" | Input == "bye" | Input == "exit")
                {
                    Application.Exit();
                }
                else if (Input.Length >= 4 && Input.Substring(0, 4) == "send")
                {
                    m_Comm.SendData(RawInput.Substring(5, Input.Length - 5));
                }
                else
                {
                    TextBoxTerminal.AppendText("ERROR: Command \"" + RawInput + "\" not found.\r\n");
                }
            }
        }
        #endregion

        #region UI Events (TabPageSettings)
        private void LLabelCheck_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            if (m_Comm.IsConnected())
            {
                m_Comm.SendData("1");
                LabelStatus.Text = "Current connection status: ONLINE.";
            }
            else
            {
                m_Comm.Run();
            }
        }

        private void TextBoxIP_TextChanged(object sender, EventArgs e)
        {
            Properties.Settings.Default.IP = TextBoxIP.Text;
            m_Comm.Stop();
            m_Comm.SetAddress(Properties.Settings.Default.IP, 5800);
            m_Comm.Run();
        }
        #endregion
    }
}
