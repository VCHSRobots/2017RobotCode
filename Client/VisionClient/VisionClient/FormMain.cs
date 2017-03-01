using System;
using System.Drawing;
using System.IO;
using System.Net.Sockets;
using System.Threading;
using System.Windows.Forms;

namespace VisionClient
{
    public partial class FormMain : Form
    {
        public FormMain()
        {
            InitializeComponent();
            Log("VisionClient started!");
        }

        //
        //Variables
        //

        int Camera = 0;
        TcpClient Client = new TcpClient();
        bool IsOnline = false;
        string ServerIP = Properties.Settings.Default.IP; 
        string RawInput = "";
        string Input = "";

        //
        //Networking and communications
        //

        private void ConnectionTimer_Tick(object sender, EventArgs e)
        {
            if (IsOnline == true)
            {
                Send("1");
                LabelStatus.Text = "Current connection status: ONLINE.";
            }
            else
            {
                Connect();
            }
        }
        private void Connect()
        {
            Log("Attempting to connect to server at \"" + ServerIP + ":5800\"...");
            try
            {
                Client.Connect(ServerIP, 5800);
                Send("C");
                System.Threading.Thread.Sleep(1000);
                Send("T");
                LabelStatus.Text = "Current connection status: ONLINE.";
                IsOnline = true;
            }
            catch (Exception e)
            {
                LabelStatus.Text = "Current connection status: OFFLINE.";
                IsOnline = false;
                Log("Failed to connect to server:\r\n" + e);
            }
        }
        private void Listen()
        {
            while (true)
            { 
                try
                {
                    NetworkStream strm = Client.GetStream();
                    StreamReader reader = new StreamReader(strm);
                    string line = reader.ReadLine();
                    byte[] pic = Convert.FromBase64String(line);
                    using (MemoryStream ms = new MemoryStream(pic))
                    {
                        PictureBox.Image = Image.FromStream(ms);
                    }
                }
                catch
                {
                    continue;
                }
            }
        }
        private void Send(string Message)
        {
            Log("Attempting to send data...");
            try
            {
                NetworkStream Stream = Client.GetStream();
                System.Text.ASCIIEncoding asen = new System.Text.ASCIIEncoding();
                byte[] ba = asen.GetBytes(Message);
                Stream.WriteAsync(ba, 0, ba.Length);
                IsOnline = true;
                LabelStatus.Text = "Current connection status: ONLINE.";
                Log("Data sent to server: " + Message);
                
            }
            catch (Exception e)
            {
                IsOnline = false;
                LabelStatus.Text = "Current connection status: OFFLINE.";
                Log("ERROR: Failed to send data to server: client offline:\r\n" + e);
            }
        }
        private void RefreshTimer_Tick(object sender, EventArgs e)
        {
            if (IsOnline == false)
            {
                LabelStatus.Text = "Current connection status: OFFLINE.";
            }
            if (IsOnline == true)
            {
                LabelStatus.Text = "Current connection status: ONLINE.";
            }
        }

        //
        //FormMain
        //

        private void FormMain_Shown(object sender, EventArgs e)
        {
            Connect();
            ConnectionTimer.Start();
            RefreshTimer.Start();
            Client.ReceiveBufferSize = 300000;
            Thread ListenThread = new Thread(Listen);
            ListenThread.IsBackground = true;
            ListenThread.Start();
            ServerIP = Properties.Settings.Default.IP;
            TextBoxIP.Text = ServerIP;
        }
        private void FormMain_FormClosed(object sender, FormClosedEventArgs e)
        {
            Log("Shutting down VisionSystem...");
            Client.Close();
            Properties.Settings.Default.Save();
        }
        private void Log(string message)
        {
            TextBoxTerminal.AppendText(message + "\r\n");
            File.WriteAllText("outlog.txt", message + "\r\n");
        }

        //
        //TabPageDisplay: Panel1
        //

        private void ButtonC0_Click(object sender, EventArgs e)
        {
            LabelCamera.Text = "Current camera: None";
            PictureBox.Image = Properties.Resources.C0;
            if (IsOnline == true)
            {
                Send("C0");
            }
        }
        private void ButtonC1_Click(object sender, EventArgs e)
        {
            if (IsOnline == true)
            {
                LabelCamera.Text = "Current camera: 1 / Front: Shooter";
                Send("C1");
            }
            else
            {
                LabelCamera.Text = "Current camera: None";
                PictureBox.Image = Properties.Resources.C0;
            }
        }
        private void ButtonC2_Click(object sender, EventArgs e)
        {
            if (IsOnline == true)
            {
                LabelCamera.Text = "Current camera: 2 / Front: General";
                Send("C2");
            }
            else
            {
                LabelCamera.Text = "Current camera: None";
                PictureBox.Image = Properties.Resources.C0;
            }
        }
        private void ButtonC3_Click(object sender, EventArgs e)
        {
            if (IsOnline == true)
            {
                LabelCamera.Text = "Current camera: 3 / Front: Gear delivery";
                Send("C3");
            }
            else
            {
                LabelCamera.Text = "Current camera: None";
                PictureBox.Image = Properties.Resources.C0;
            }
        }
        private void ButtonC4_Click(object sender, EventArgs e)
        {
            if (IsOnline == true)
            {
                LabelCamera.Text = "Current camera: 4 / Front: Rope climber";
                Send("C4");
            }
            else
            {
                LabelCamera.Text = "Current camera: None";
                PictureBox.Image = Properties.Resources.C0;
            }
        }

        //
        //TabPageDisplay: Panel2
        //

        private void ButtonAimStop_Click(object sender, EventArgs e)
        {
            if (IsOnline == true)
            {
                Send("T0");
            }
            else
            {

            }
        }

        private void ButtonAimPeg_Click(object sender, EventArgs e)
        {
            if (IsOnline == true)
            {
                Send("T2");
            }
            else
            {

            }
        }

        private void ButtonAimBoiler_Click(object sender, EventArgs e)
        {
            if (IsOnline == true)
            {
                Send("T1");
            }
            else
            {

            }
        }

        //
        //TabPageTerminal
        //

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
                    if (IsOnline == true)
                    {
                        Send("1");
                        LabelStatus.Text = "Current connection status: ONLINE.";
                    }
                    else
                    {
                        Connect();
                    }
                }
                else if (Input == "disconnect")
                {
                    if (IsOnline == true)
                    {
                        Client.Close();
                        TextBoxTerminal.AppendText("Disconnected. Please note that you will not be able to reconnect for several minutes, due to underlying networking protocols.\r\n");
                        IsOnline = false;
                    }
                    else
                    {
                        try
                        {
                            Client.Close();
                        }
                        catch
                        {
                            //Do nothing
                        }
                        Log("ERROR: Unable to disconnect: client is not connected.");
                    }
                }
                else if (Input == "quit" | Input == "bye" | Input == "exit")
                {
                    Application.Exit();
                }
                else if (Input.Length >= 4 && Input.Substring(0, 4) == "send")
                {
                    Send(RawInput.Substring(5, Input.Length - 5));
                }
                else
                {
                    TextBoxTerminal.AppendText("ERROR: Command \"" + RawInput + "\" not found.\r\n");
                }
            }
        }

        //
        //TabPageSettings
        //
        private void LLabelCheck_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            if (IsOnline == true)
            {
                Send("1");
                LabelStatus.Text = "Current connection status: ONLINE.";
            }
            else
            {
                Connect();
            }
        }
        private void TextBoxIP_TextChanged(object sender, EventArgs e)
        {
            Properties.Settings.Default.IP = TextBoxIP.Text;
            ServerIP = TextBoxIP.Text;
        }
    }
}
