namespace MqttShow
{
    partial class MainForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.textBox_MainLog = new System.Windows.Forms.TextBox();
            this.notifyIcon1 = new System.Windows.Forms.NotifyIcon(this.components);
            this.label_ConnectionStatus = new System.Windows.Forms.Label();
            this.tabControlMain = new System.Windows.Forms.TabControl();
            this.tabPageGeneral = new System.Windows.Forms.TabPage();
            this.tabPageRobot = new System.Windows.Forms.TabPage();
            this.textBoxRobotLog = new System.Windows.Forms.TextBox();
            this.tabPageJetson = new System.Windows.Forms.TabPage();
            this.textBoxJetsonLog = new System.Windows.Forms.TextBox();
            this.tabPageMqttLog = new System.Windows.Forms.TabPage();
            this.textBoxMqttLog = new System.Windows.Forms.TextBox();
            this.textBox1 = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.textBox2 = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.textBox3 = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.textBox4 = new System.Windows.Forms.TextBox();
            this.buttonSendParams = new System.Windows.Forms.Button();
            this.pictureBoxTarget = new System.Windows.Forms.PictureBox();
            this.panel1 = new System.Windows.Forms.Panel();
            this.radioButtonBlueSide = new System.Windows.Forms.RadioButton();
            this.radioButtonRedSide = new System.Windows.Forms.RadioButton();
            this.label6 = new System.Windows.Forms.Label();
            this.panel3 = new System.Windows.Forms.Panel();
            this.radioButtonBinAndShoot = new System.Windows.Forms.RadioButton();
            this.radioButtonSideGearAndShoot = new System.Windows.Forms.RadioButton();
            this.radioButtonMoveForward = new System.Windows.Forms.RadioButton();
            this.radioButtonCenterGearAndShoot = new System.Windows.Forms.RadioButton();
            this.radioButtonCenterGear = new System.Windows.Forms.RadioButton();
            this.label7 = new System.Windows.Forms.Label();
            this.linkLabelClearGeneral = new System.Windows.Forms.LinkLabel();
            this.linkLabelClearRobot = new System.Windows.Forms.LinkLabel();
            this.linkLabelClearJetson = new System.Windows.Forms.LinkLabel();
            this.linkLabelClearMqtt = new System.Windows.Forms.LinkLabel();
            this.panelClearBox = new System.Windows.Forms.Panel();
            this.tabPagePID = new System.Windows.Forms.TabPage();
            this.dataGridView1 = new System.Windows.Forms.DataGridView();
            this.label1 = new System.Windows.Forms.Label();
            this.linkLabelSendPIDs = new System.Windows.Forms.LinkLabel();
            this.tabPageTarSys = new System.Windows.Forms.TabPage();
            this.PidName = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.PidSP1 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.PidSP2 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.PidTLow = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.PidTHigh = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.PidGain = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.PidD = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.PidI = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.linkLabelSendAuto = new System.Windows.Forms.LinkLabel();
            this.tabControlMain.SuspendLayout();
            this.tabPageGeneral.SuspendLayout();
            this.tabPageRobot.SuspendLayout();
            this.tabPageJetson.SuspendLayout();
            this.tabPageMqttLog.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxTarget)).BeginInit();
            this.panel1.SuspendLayout();
            this.panel3.SuspendLayout();
            this.panelClearBox.SuspendLayout();
            this.tabPagePID.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView1)).BeginInit();
            this.tabPageTarSys.SuspendLayout();
            this.SuspendLayout();
            // 
            // textBox_MainLog
            // 
            this.textBox_MainLog.Dock = System.Windows.Forms.DockStyle.Fill;
            this.textBox_MainLog.Font = new System.Drawing.Font("Courier New", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBox_MainLog.Location = new System.Drawing.Point(3, 3);
            this.textBox_MainLog.Multiline = true;
            this.textBox_MainLog.Name = "textBox_MainLog";
            this.textBox_MainLog.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.textBox_MainLog.Size = new System.Drawing.Size(492, 426);
            this.textBox_MainLog.TabIndex = 0;
            this.textBox_MainLog.WordWrap = false;
            // 
            // notifyIcon1
            // 
            this.notifyIcon1.Text = "notifyIcon1";
            this.notifyIcon1.Visible = true;
            // 
            // label_ConnectionStatus
            // 
            this.label_ConnectionStatus.AutoSize = true;
            this.label_ConnectionStatus.Font = new System.Drawing.Font("Microsoft Sans Serif", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_ConnectionStatus.ForeColor = System.Drawing.Color.DarkGreen;
            this.label_ConnectionStatus.Location = new System.Drawing.Point(12, 9);
            this.label_ConnectionStatus.Name = "label_ConnectionStatus";
            this.label_ConnectionStatus.Size = new System.Drawing.Size(116, 25);
            this.label_ConnectionStatus.TabIndex = 2;
            this.label_ConnectionStatus.Text = "Connected";
            // 
            // tabControlMain
            // 
            this.tabControlMain.Controls.Add(this.tabPageGeneral);
            this.tabControlMain.Controls.Add(this.tabPageRobot);
            this.tabControlMain.Controls.Add(this.tabPageJetson);
            this.tabControlMain.Controls.Add(this.tabPageMqttLog);
            this.tabControlMain.Controls.Add(this.tabPageTarSys);
            this.tabControlMain.Controls.Add(this.tabPagePID);
            this.tabControlMain.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.tabControlMain.Location = new System.Drawing.Point(398, 34);
            this.tabControlMain.Name = "tabControlMain";
            this.tabControlMain.SelectedIndex = 0;
            this.tabControlMain.Size = new System.Drawing.Size(506, 461);
            this.tabControlMain.TabIndex = 4;
            // 
            // tabPageGeneral
            // 
            this.tabPageGeneral.Controls.Add(this.textBox_MainLog);
            this.tabPageGeneral.Location = new System.Drawing.Point(4, 25);
            this.tabPageGeneral.Name = "tabPageGeneral";
            this.tabPageGeneral.Padding = new System.Windows.Forms.Padding(3);
            this.tabPageGeneral.Size = new System.Drawing.Size(498, 432);
            this.tabPageGeneral.TabIndex = 0;
            this.tabPageGeneral.Text = "General Log";
            this.tabPageGeneral.UseVisualStyleBackColor = true;
            // 
            // tabPageRobot
            // 
            this.tabPageRobot.Controls.Add(this.textBoxRobotLog);
            this.tabPageRobot.Location = new System.Drawing.Point(4, 25);
            this.tabPageRobot.Name = "tabPageRobot";
            this.tabPageRobot.Padding = new System.Windows.Forms.Padding(3);
            this.tabPageRobot.Size = new System.Drawing.Size(498, 432);
            this.tabPageRobot.TabIndex = 1;
            this.tabPageRobot.Text = "Robot Log";
            this.tabPageRobot.UseVisualStyleBackColor = true;
            // 
            // textBoxRobotLog
            // 
            this.textBoxRobotLog.Dock = System.Windows.Forms.DockStyle.Fill;
            this.textBoxRobotLog.Font = new System.Drawing.Font("Courier New", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBoxRobotLog.Location = new System.Drawing.Point(3, 3);
            this.textBoxRobotLog.Multiline = true;
            this.textBoxRobotLog.Name = "textBoxRobotLog";
            this.textBoxRobotLog.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.textBoxRobotLog.Size = new System.Drawing.Size(492, 426);
            this.textBoxRobotLog.TabIndex = 1;
            this.textBoxRobotLog.WordWrap = false;
            // 
            // tabPageJetson
            // 
            this.tabPageJetson.Controls.Add(this.textBoxJetsonLog);
            this.tabPageJetson.Location = new System.Drawing.Point(4, 25);
            this.tabPageJetson.Name = "tabPageJetson";
            this.tabPageJetson.Size = new System.Drawing.Size(498, 432);
            this.tabPageJetson.TabIndex = 2;
            this.tabPageJetson.Text = "Jetson Log";
            this.tabPageJetson.UseVisualStyleBackColor = true;
            // 
            // textBoxJetsonLog
            // 
            this.textBoxJetsonLog.Dock = System.Windows.Forms.DockStyle.Fill;
            this.textBoxJetsonLog.Location = new System.Drawing.Point(0, 0);
            this.textBoxJetsonLog.Multiline = true;
            this.textBoxJetsonLog.Name = "textBoxJetsonLog";
            this.textBoxJetsonLog.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.textBoxJetsonLog.Size = new System.Drawing.Size(498, 432);
            this.textBoxJetsonLog.TabIndex = 2;
            this.textBoxJetsonLog.WordWrap = false;
            // 
            // tabPageMqttLog
            // 
            this.tabPageMqttLog.Controls.Add(this.textBoxMqttLog);
            this.tabPageMqttLog.Location = new System.Drawing.Point(4, 25);
            this.tabPageMqttLog.Name = "tabPageMqttLog";
            this.tabPageMqttLog.Size = new System.Drawing.Size(498, 432);
            this.tabPageMqttLog.TabIndex = 3;
            this.tabPageMqttLog.Text = "Mqtt Log";
            this.tabPageMqttLog.UseVisualStyleBackColor = true;
            // 
            // textBoxMqttLog
            // 
            this.textBoxMqttLog.Dock = System.Windows.Forms.DockStyle.Fill;
            this.textBoxMqttLog.Location = new System.Drawing.Point(0, 0);
            this.textBoxMqttLog.Multiline = true;
            this.textBoxMqttLog.Name = "textBoxMqttLog";
            this.textBoxMqttLog.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.textBoxMqttLog.Size = new System.Drawing.Size(498, 432);
            this.textBoxMqttLog.TabIndex = 1;
            this.textBoxMqttLog.WordWrap = false;
            // 
            // textBox1
            // 
            this.textBox1.Location = new System.Drawing.Point(83, 25);
            this.textBox1.Name = "textBox1";
            this.textBox1.Size = new System.Drawing.Size(100, 22);
            this.textBox1.TabIndex = 5;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(30, 59);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(55, 16);
            this.label2.TabIndex = 8;
            this.label2.Text = "Param2";
            // 
            // textBox2
            // 
            this.textBox2.Location = new System.Drawing.Point(83, 59);
            this.textBox2.Name = "textBox2";
            this.textBox2.Size = new System.Drawing.Size(100, 22);
            this.textBox2.TabIndex = 7;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(30, 28);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(55, 16);
            this.label3.TabIndex = 6;
            this.label3.Text = "Param1";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(30, 129);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(55, 16);
            this.label4.TabIndex = 12;
            this.label4.Text = "Param4";
            // 
            // textBox3
            // 
            this.textBox3.Location = new System.Drawing.Point(83, 95);
            this.textBox3.Name = "textBox3";
            this.textBox3.Size = new System.Drawing.Size(100, 22);
            this.textBox3.TabIndex = 11;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(30, 98);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(55, 16);
            this.label5.TabIndex = 10;
            this.label5.Text = "Param3";
            // 
            // textBox4
            // 
            this.textBox4.Location = new System.Drawing.Point(83, 126);
            this.textBox4.Name = "textBox4";
            this.textBox4.Size = new System.Drawing.Size(100, 22);
            this.textBox4.TabIndex = 9;
            // 
            // buttonSendParams
            // 
            this.buttonSendParams.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonSendParams.Location = new System.Drawing.Point(46, 162);
            this.buttonSendParams.Name = "buttonSendParams";
            this.buttonSendParams.Size = new System.Drawing.Size(100, 30);
            this.buttonSendParams.TabIndex = 13;
            this.buttonSendParams.Text = "Send";
            this.buttonSendParams.UseVisualStyleBackColor = true;
            // 
            // pictureBoxTarget
            // 
            this.pictureBoxTarget.Location = new System.Drawing.Point(17, 154);
            this.pictureBoxTarget.Name = "pictureBoxTarget";
            this.pictureBoxTarget.Size = new System.Drawing.Size(364, 331);
            this.pictureBoxTarget.TabIndex = 14;
            this.pictureBoxTarget.TabStop = false;
            // 
            // panel1
            // 
            this.panel1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.panel1.Controls.Add(this.radioButtonBlueSide);
            this.panel1.Controls.Add(this.radioButtonRedSide);
            this.panel1.Controls.Add(this.label6);
            this.panel1.Location = new System.Drawing.Point(29, 67);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(124, 70);
            this.panel1.TabIndex = 16;
            // 
            // radioButtonBlueSide
            // 
            this.radioButtonBlueSide.AutoSize = true;
            this.radioButtonBlueSide.Checked = true;
            this.radioButtonBlueSide.Location = new System.Drawing.Point(17, 46);
            this.radioButtonBlueSide.Name = "radioButtonBlueSide";
            this.radioButtonBlueSide.Size = new System.Drawing.Size(70, 17);
            this.radioButtonBlueSide.TabIndex = 2;
            this.radioButtonBlueSide.TabStop = true;
            this.radioButtonBlueSide.Text = "Blue Side";
            this.radioButtonBlueSide.UseVisualStyleBackColor = true;
            this.radioButtonBlueSide.CheckedChanged += new System.EventHandler(this.radioButtonBlueSide_CheckedChanged);
            // 
            // radioButtonRedSide
            // 
            this.radioButtonRedSide.AutoSize = true;
            this.radioButtonRedSide.Location = new System.Drawing.Point(17, 23);
            this.radioButtonRedSide.Name = "radioButtonRedSide";
            this.radioButtonRedSide.Size = new System.Drawing.Size(69, 17);
            this.radioButtonRedSide.TabIndex = 1;
            this.radioButtonRedSide.Text = "Red Side";
            this.radioButtonRedSide.UseVisualStyleBackColor = true;
            this.radioButtonRedSide.CheckedChanged += new System.EventHandler(this.radioButtonRedSide_CheckedChanged);
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label6.Location = new System.Drawing.Point(14, 6);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(105, 13);
            this.label6.TabIndex = 0;
            this.label6.Text = "Autonomous Side";
            // 
            // panel3
            // 
            this.panel3.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.panel3.Controls.Add(this.radioButtonBinAndShoot);
            this.panel3.Controls.Add(this.radioButtonSideGearAndShoot);
            this.panel3.Controls.Add(this.radioButtonMoveForward);
            this.panel3.Controls.Add(this.radioButtonCenterGearAndShoot);
            this.panel3.Controls.Add(this.radioButtonCenterGear);
            this.panel3.Controls.Add(this.label7);
            this.panel3.Location = new System.Drawing.Point(159, 13);
            this.panel3.Name = "panel3";
            this.panel3.Size = new System.Drawing.Size(154, 124);
            this.panel3.TabIndex = 16;
            // 
            // radioButtonBinAndShoot
            // 
            this.radioButtonBinAndShoot.AutoSize = true;
            this.radioButtonBinAndShoot.Location = new System.Drawing.Point(4, 97);
            this.radioButtonBinAndShoot.Name = "radioButtonBinAndShoot";
            this.radioButtonBinAndShoot.Size = new System.Drawing.Size(92, 17);
            this.radioButtonBinAndShoot.TabIndex = 5;
            this.radioButtonBinAndShoot.Text = "Bin and Shoot";
            this.radioButtonBinAndShoot.UseVisualStyleBackColor = true;
            this.radioButtonBinAndShoot.CheckedChanged += new System.EventHandler(this.radioButtonBinAndShoot_CheckedChanged);
            // 
            // radioButtonSideGearAndShoot
            // 
            this.radioButtonSideGearAndShoot.AutoSize = true;
            this.radioButtonSideGearAndShoot.Location = new System.Drawing.Point(5, 78);
            this.radioButtonSideGearAndShoot.Name = "radioButtonSideGearAndShoot";
            this.radioButtonSideGearAndShoot.Size = new System.Drawing.Size(124, 17);
            this.radioButtonSideGearAndShoot.TabIndex = 4;
            this.radioButtonSideGearAndShoot.Text = "Side Gear and Shoot";
            this.radioButtonSideGearAndShoot.UseVisualStyleBackColor = true;
            this.radioButtonSideGearAndShoot.CheckedChanged += new System.EventHandler(this.radioButtonSideGearAndShoot_CheckedChanged);
            // 
            // radioButtonMoveForward
            // 
            this.radioButtonMoveForward.AutoSize = true;
            this.radioButtonMoveForward.Location = new System.Drawing.Point(6, 22);
            this.radioButtonMoveForward.Name = "radioButtonMoveForward";
            this.radioButtonMoveForward.Size = new System.Drawing.Size(93, 17);
            this.radioButtonMoveForward.TabIndex = 3;
            this.radioButtonMoveForward.Text = "Move Forward";
            this.radioButtonMoveForward.UseVisualStyleBackColor = true;
            this.radioButtonMoveForward.CheckedChanged += new System.EventHandler(this.radioButtonMoveForward_CheckedChanged);
            // 
            // radioButtonCenterGearAndShoot
            // 
            this.radioButtonCenterGearAndShoot.AutoSize = true;
            this.radioButtonCenterGearAndShoot.Checked = true;
            this.radioButtonCenterGearAndShoot.Location = new System.Drawing.Point(6, 59);
            this.radioButtonCenterGearAndShoot.Name = "radioButtonCenterGearAndShoot";
            this.radioButtonCenterGearAndShoot.Size = new System.Drawing.Size(122, 17);
            this.radioButtonCenterGearAndShoot.TabIndex = 2;
            this.radioButtonCenterGearAndShoot.TabStop = true;
            this.radioButtonCenterGearAndShoot.Text = "Cntr Gear and Shoot";
            this.radioButtonCenterGearAndShoot.UseVisualStyleBackColor = true;
            this.radioButtonCenterGearAndShoot.CheckedChanged += new System.EventHandler(this.radioButtonCenterGearAndShoot_CheckedChanged);
            // 
            // radioButtonCenterGear
            // 
            this.radioButtonCenterGear.AutoSize = true;
            this.radioButtonCenterGear.Location = new System.Drawing.Point(6, 39);
            this.radioButtonCenterGear.Name = "radioButtonCenterGear";
            this.radioButtonCenterGear.Size = new System.Drawing.Size(82, 17);
            this.radioButtonCenterGear.TabIndex = 1;
            this.radioButtonCenterGear.Text = "Center Gear";
            this.radioButtonCenterGear.UseVisualStyleBackColor = true;
            this.radioButtonCenterGear.CheckedChanged += new System.EventHandler(this.radioButtonCenterGear_CheckedChanged);
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label7.Location = new System.Drawing.Point(14, 6);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(126, 13);
            this.label7.TabIndex = 0;
            this.label7.Text = "Autonomous Program";
            // 
            // linkLabelClearGeneral
            // 
            this.linkLabelClearGeneral.AutoSize = true;
            this.linkLabelClearGeneral.Location = new System.Drawing.Point(5, 5);
            this.linkLabelClearGeneral.Name = "linkLabelClearGeneral";
            this.linkLabelClearGeneral.Size = new System.Drawing.Size(54, 13);
            this.linkLabelClearGeneral.TabIndex = 17;
            this.linkLabelClearGeneral.TabStop = true;
            this.linkLabelClearGeneral.Text = "Clear Gen";
            this.linkLabelClearGeneral.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.linkLabelClearGeneral_LinkClicked);
            // 
            // linkLabelClearRobot
            // 
            this.linkLabelClearRobot.AutoSize = true;
            this.linkLabelClearRobot.Location = new System.Drawing.Point(90, 5);
            this.linkLabelClearRobot.Name = "linkLabelClearRobot";
            this.linkLabelClearRobot.Size = new System.Drawing.Size(63, 13);
            this.linkLabelClearRobot.TabIndex = 18;
            this.linkLabelClearRobot.TabStop = true;
            this.linkLabelClearRobot.Text = "Clear Robot";
            this.linkLabelClearRobot.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.linkLabelClearRobot_LinkClicked);
            // 
            // linkLabelClearJetson
            // 
            this.linkLabelClearJetson.AutoSize = true;
            this.linkLabelClearJetson.Location = new System.Drawing.Point(168, 5);
            this.linkLabelClearJetson.Name = "linkLabelClearJetson";
            this.linkLabelClearJetson.Size = new System.Drawing.Size(65, 13);
            this.linkLabelClearJetson.TabIndex = 19;
            this.linkLabelClearJetson.TabStop = true;
            this.linkLabelClearJetson.Text = "Clear Jetson";
            this.linkLabelClearJetson.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.linkLabelClearJetson_LinkClicked);
            // 
            // linkLabelClearMqtt
            // 
            this.linkLabelClearMqtt.AutoSize = true;
            this.linkLabelClearMqtt.Location = new System.Drawing.Point(239, 5);
            this.linkLabelClearMqtt.Name = "linkLabelClearMqtt";
            this.linkLabelClearMqtt.Size = new System.Drawing.Size(55, 13);
            this.linkLabelClearMqtt.TabIndex = 20;
            this.linkLabelClearMqtt.TabStop = true;
            this.linkLabelClearMqtt.Text = "Clear Mqtt";
            this.linkLabelClearMqtt.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.linkLabelClearMqtt_LinkClicked);
            // 
            // panelClearBox
            // 
            this.panelClearBox.Controls.Add(this.linkLabelClearMqtt);
            this.panelClearBox.Controls.Add(this.linkLabelClearJetson);
            this.panelClearBox.Controls.Add(this.linkLabelClearRobot);
            this.panelClearBox.Controls.Add(this.linkLabelClearGeneral);
            this.panelClearBox.Location = new System.Drawing.Point(401, 3);
            this.panelClearBox.Name = "panelClearBox";
            this.panelClearBox.Size = new System.Drawing.Size(325, 25);
            this.panelClearBox.TabIndex = 21;
            // 
            // tabPagePID
            // 
            this.tabPagePID.Controls.Add(this.linkLabelSendPIDs);
            this.tabPagePID.Controls.Add(this.label1);
            this.tabPagePID.Controls.Add(this.dataGridView1);
            this.tabPagePID.Location = new System.Drawing.Point(4, 25);
            this.tabPagePID.Name = "tabPagePID";
            this.tabPagePID.Size = new System.Drawing.Size(498, 432);
            this.tabPagePID.TabIndex = 4;
            this.tabPagePID.Text = "PID Params";
            this.tabPagePID.UseVisualStyleBackColor = true;
            // 
            // dataGridView1
            // 
            this.dataGridView1.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView1.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.PidName,
            this.PidSP1,
            this.PidSP2,
            this.PidTLow,
            this.PidTHigh,
            this.PidGain,
            this.PidD,
            this.PidI});
            this.dataGridView1.Location = new System.Drawing.Point(7, 62);
            this.dataGridView1.Name = "dataGridView1";
            this.dataGridView1.Size = new System.Drawing.Size(483, 367);
            this.dataGridView1.TabIndex = 0;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(93, 25);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(253, 25);
            this.label1.TabIndex = 1;
            this.label1.Text = "NOT IMPLIMENTED YET";
            // 
            // linkLabelSendPIDs
            // 
            this.linkLabelSendPIDs.AutoSize = true;
            this.linkLabelSendPIDs.Location = new System.Drawing.Point(18, 22);
            this.linkLabelSendPIDs.Name = "linkLabelSendPIDs";
            this.linkLabelSendPIDs.Size = new System.Drawing.Size(40, 16);
            this.linkLabelSendPIDs.TabIndex = 2;
            this.linkLabelSendPIDs.TabStop = true;
            this.linkLabelSendPIDs.Text = "Send";
            // 
            // tabPageTarSys
            // 
            this.tabPageTarSys.Controls.Add(this.textBox3);
            this.tabPageTarSys.Controls.Add(this.textBox1);
            this.tabPageTarSys.Controls.Add(this.label3);
            this.tabPageTarSys.Controls.Add(this.textBox2);
            this.tabPageTarSys.Controls.Add(this.buttonSendParams);
            this.tabPageTarSys.Controls.Add(this.label2);
            this.tabPageTarSys.Controls.Add(this.label4);
            this.tabPageTarSys.Controls.Add(this.textBox4);
            this.tabPageTarSys.Controls.Add(this.label5);
            this.tabPageTarSys.Location = new System.Drawing.Point(4, 25);
            this.tabPageTarSys.Name = "tabPageTarSys";
            this.tabPageTarSys.Size = new System.Drawing.Size(498, 432);
            this.tabPageTarSys.TabIndex = 5;
            this.tabPageTarSys.Text = "TargSys";
            this.tabPageTarSys.UseVisualStyleBackColor = true;
            // 
            // PidName
            // 
            this.PidName.HeaderText = "Name";
            this.PidName.Name = "PidName";
            // 
            // PidSP1
            // 
            this.PidSP1.HeaderText = "SP1";
            this.PidSP1.Name = "PidSP1";
            // 
            // PidSP2
            // 
            this.PidSP2.HeaderText = "SP2";
            this.PidSP2.Name = "PidSP2";
            // 
            // PidTLow
            // 
            this.PidTLow.HeaderText = "TLow";
            this.PidTLow.Name = "PidTLow";
            // 
            // PidTHigh
            // 
            this.PidTHigh.HeaderText = "THigh";
            this.PidTHigh.Name = "PidTHigh";
            // 
            // PidGain
            // 
            this.PidGain.HeaderText = "Gain";
            this.PidGain.Name = "PidGain";
            // 
            // PidD
            // 
            this.PidD.HeaderText = "D";
            this.PidD.Name = "PidD";
            // 
            // PidI
            // 
            this.PidI.HeaderText = "I";
            this.PidI.Name = "PidI";
            // 
            // linkLabelSendAuto
            // 
            this.linkLabelSendAuto.AutoSize = true;
            this.linkLabelSendAuto.Location = new System.Drawing.Point(28, 45);
            this.linkLabelSendAuto.Name = "linkLabelSendAuto";
            this.linkLabelSendAuto.Size = new System.Drawing.Size(32, 13);
            this.linkLabelSendAuto.TabIndex = 22;
            this.linkLabelSendAuto.TabStop = true;
            this.linkLabelSendAuto.Text = "Send";
            this.linkLabelSendAuto.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.linkLabelSendAuto_LinkClicked);
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(916, 501);
            this.Controls.Add(this.linkLabelSendAuto);
            this.Controls.Add(this.panelClearBox);
            this.Controls.Add(this.panel1);
            this.Controls.Add(this.panel3);
            this.Controls.Add(this.pictureBoxTarget);
            this.Controls.Add(this.tabControlMain);
            this.Controls.Add(this.label_ConnectionStatus);
            this.Name = "MainForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.Manual;
            this.Text = "MQTT Show";
            this.tabControlMain.ResumeLayout(false);
            this.tabPageGeneral.ResumeLayout(false);
            this.tabPageGeneral.PerformLayout();
            this.tabPageRobot.ResumeLayout(false);
            this.tabPageRobot.PerformLayout();
            this.tabPageJetson.ResumeLayout(false);
            this.tabPageJetson.PerformLayout();
            this.tabPageMqttLog.ResumeLayout(false);
            this.tabPageMqttLog.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxTarget)).EndInit();
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            this.panel3.ResumeLayout(false);
            this.panel3.PerformLayout();
            this.panelClearBox.ResumeLayout(false);
            this.panelClearBox.PerformLayout();
            this.tabPagePID.ResumeLayout(false);
            this.tabPagePID.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView1)).EndInit();
            this.tabPageTarSys.ResumeLayout(false);
            this.tabPageTarSys.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox textBox_MainLog;
        private System.Windows.Forms.NotifyIcon notifyIcon1;
        private System.Windows.Forms.Label label_ConnectionStatus;
        private System.Windows.Forms.TabControl tabControlMain;
        private System.Windows.Forms.TabPage tabPageGeneral;
        private System.Windows.Forms.TabPage tabPageRobot;
        private System.Windows.Forms.TextBox textBox1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox textBox2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox textBox3;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.TextBox textBox4;
        private System.Windows.Forms.Button buttonSendParams;
        private System.Windows.Forms.PictureBox pictureBoxTarget;
        private System.Windows.Forms.TextBox textBoxRobotLog;
        private System.Windows.Forms.TabPage tabPageJetson;
        private System.Windows.Forms.TextBox textBoxJetsonLog;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.RadioButton radioButtonBlueSide;
        private System.Windows.Forms.RadioButton radioButtonRedSide;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Panel panel3;
        private System.Windows.Forms.RadioButton radioButtonBinAndShoot;
        private System.Windows.Forms.RadioButton radioButtonSideGearAndShoot;
        private System.Windows.Forms.RadioButton radioButtonMoveForward;
        private System.Windows.Forms.RadioButton radioButtonCenterGearAndShoot;
        private System.Windows.Forms.RadioButton radioButtonCenterGear;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.TabPage tabPageMqttLog;
        private System.Windows.Forms.TextBox textBoxMqttLog;
        private System.Windows.Forms.LinkLabel linkLabelClearGeneral;
        private System.Windows.Forms.LinkLabel linkLabelClearRobot;
        private System.Windows.Forms.LinkLabel linkLabelClearJetson;
        private System.Windows.Forms.LinkLabel linkLabelClearMqtt;
        private System.Windows.Forms.Panel panelClearBox;
        private System.Windows.Forms.TabPage tabPageTarSys;
        private System.Windows.Forms.TabPage tabPagePID;
        private System.Windows.Forms.LinkLabel linkLabelSendPIDs;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.DataGridView dataGridView1;
        private System.Windows.Forms.DataGridViewTextBoxColumn PidName;
        private System.Windows.Forms.DataGridViewTextBoxColumn PidSP1;
        private System.Windows.Forms.DataGridViewTextBoxColumn PidSP2;
        private System.Windows.Forms.DataGridViewTextBoxColumn PidTLow;
        private System.Windows.Forms.DataGridViewTextBoxColumn PidTHigh;
        private System.Windows.Forms.DataGridViewTextBoxColumn PidGain;
        private System.Windows.Forms.DataGridViewTextBoxColumn PidD;
        private System.Windows.Forms.DataGridViewTextBoxColumn PidI;
        private System.Windows.Forms.LinkLabel linkLabelSendAuto;
    }
}

