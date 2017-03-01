namespace VisionClient
{
    partial class FormMain
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(FormMain));
            this.TabControl = new System.Windows.Forms.TabControl();
            this.TabPageDisplay = new System.Windows.Forms.TabPage();
            this.SplitContainer = new System.Windows.Forms.SplitContainer();
            this.LabelCamera = new System.Windows.Forms.Label();
            this.ButtonC1 = new System.Windows.Forms.Button();
            this.ButtonC2 = new System.Windows.Forms.Button();
            this.ButtonC3 = new System.Windows.Forms.Button();
            this.ButtonC0 = new System.Windows.Forms.Button();
            this.ButtonC4 = new System.Windows.Forms.Button();
            this.PictureBox = new System.Windows.Forms.PictureBox();
            this.ButtonAimBoiler = new System.Windows.Forms.Button();
            this.ButtonAimPeg = new System.Windows.Forms.Button();
            this.ButtonAimStop = new System.Windows.Forms.Button();
            this.TabPageTerminal = new System.Windows.Forms.TabPage();
            this.TextBoxTerminalInput = new System.Windows.Forms.TextBox();
            this.TextBoxTerminal = new System.Windows.Forms.TextBox();
            this.TabPageSettings = new System.Windows.Forms.TabPage();
            this.LabelControllerCameraKeys = new System.Windows.Forms.Label();
            this.TextBoxIP = new System.Windows.Forms.TextBox();
            this.LabelServerIP = new System.Windows.Forms.Label();
            this.TabPageAbout = new System.Windows.Forms.TabPage();
            this.LinkLabelCheckConnection = new System.Windows.Forms.LinkLabel();
            this.LabelStatus = new System.Windows.Forms.Label();
            this.RefreshTimer = new System.Windows.Forms.Timer(this.components);
            this.ConnectionTimer = new System.Windows.Forms.Timer(this.components);
            this.PictureBoxFieldOverview = new System.Windows.Forms.PictureBox();
            this.TabControl.SuspendLayout();
            this.TabPageDisplay.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.SplitContainer)).BeginInit();
            this.SplitContainer.Panel1.SuspendLayout();
            this.SplitContainer.Panel2.SuspendLayout();
            this.SplitContainer.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.PictureBox)).BeginInit();
            this.TabPageTerminal.SuspendLayout();
            this.TabPageSettings.SuspendLayout();
            this.TabPageAbout.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.PictureBoxFieldOverview)).BeginInit();
            this.SuspendLayout();
            // 
            // TabControl
            // 
            this.TabControl.Controls.Add(this.TabPageDisplay);
            this.TabControl.Controls.Add(this.TabPageTerminal);
            this.TabControl.Controls.Add(this.TabPageSettings);
            this.TabControl.Controls.Add(this.TabPageAbout);
            this.TabControl.Dock = System.Windows.Forms.DockStyle.Fill;
            this.TabControl.Location = new System.Drawing.Point(0, 0);
            this.TabControl.Name = "TabControl";
            this.TabControl.SelectedIndex = 0;
            this.TabControl.Size = new System.Drawing.Size(1264, 761);
            this.TabControl.TabIndex = 0;
            this.TabControl.SelectedIndexChanged += new System.EventHandler(this.TabControl_SelectedIndexChanged);
            // 
            // TabPageDisplay
            // 
            this.TabPageDisplay.Controls.Add(this.SplitContainer);
            this.TabPageDisplay.Location = new System.Drawing.Point(4, 22);
            this.TabPageDisplay.Name = "TabPageDisplay";
            this.TabPageDisplay.Padding = new System.Windows.Forms.Padding(3);
            this.TabPageDisplay.Size = new System.Drawing.Size(1256, 735);
            this.TabPageDisplay.TabIndex = 0;
            this.TabPageDisplay.Text = "Display";
            this.TabPageDisplay.UseVisualStyleBackColor = true;
            // 
            // SplitContainer
            // 
            this.SplitContainer.BackColor = System.Drawing.SystemColors.ControlDark;
            this.SplitContainer.Dock = System.Windows.Forms.DockStyle.Fill;
            this.SplitContainer.Location = new System.Drawing.Point(3, 3);
            this.SplitContainer.Name = "SplitContainer";
            // 
            // SplitContainer.Panel1
            // 
            this.SplitContainer.Panel1.BackColor = System.Drawing.SystemColors.Control;
            this.SplitContainer.Panel1.Controls.Add(this.LabelCamera);
            this.SplitContainer.Panel1.Controls.Add(this.ButtonC1);
            this.SplitContainer.Panel1.Controls.Add(this.ButtonC2);
            this.SplitContainer.Panel1.Controls.Add(this.ButtonC3);
            this.SplitContainer.Panel1.Controls.Add(this.ButtonC0);
            this.SplitContainer.Panel1.Controls.Add(this.ButtonC4);
            this.SplitContainer.Panel1.Controls.Add(this.PictureBox);
            this.SplitContainer.Panel1MinSize = 625;
            // 
            // SplitContainer.Panel2
            // 
            this.SplitContainer.Panel2.BackColor = System.Drawing.SystemColors.ControlLight;
            this.SplitContainer.Panel2.Controls.Add(this.PictureBoxFieldOverview);
            this.SplitContainer.Panel2.Controls.Add(this.ButtonAimBoiler);
            this.SplitContainer.Panel2.Controls.Add(this.ButtonAimPeg);
            this.SplitContainer.Panel2.Controls.Add(this.ButtonAimStop);
            this.SplitContainer.Panel2MinSize = 8;
            this.SplitContainer.Size = new System.Drawing.Size(1250, 729);
            this.SplitContainer.SplitterDistance = 625;
            this.SplitContainer.SplitterWidth = 8;
            this.SplitContainer.TabIndex = 0;
            // 
            // LabelCamera
            // 
            this.LabelCamera.AutoSize = true;
            this.LabelCamera.BackColor = System.Drawing.Color.Black;
            this.LabelCamera.ForeColor = System.Drawing.Color.White;
            this.LabelCamera.Location = new System.Drawing.Point(5, 13);
            this.LabelCamera.Name = "LabelCamera";
            this.LabelCamera.Size = new System.Drawing.Size(111, 13);
            this.LabelCamera.TabIndex = 6;
            this.LabelCamera.Text = "Current camera: None";
            // 
            // ButtonC1
            // 
            this.ButtonC1.Anchor = System.Windows.Forms.AnchorStyles.Bottom;
            this.ButtonC1.Cursor = System.Windows.Forms.Cursors.Hand;
            this.ButtonC1.Location = new System.Drawing.Point(131, 632);
            this.ButtonC1.Name = "ButtonC1";
            this.ButtonC1.Size = new System.Drawing.Size(105, 90);
            this.ButtonC1.TabIndex = 5;
            this.ButtonC1.Text = "Camera 1: Front: Shooter";
            this.ButtonC1.UseVisualStyleBackColor = true;
            this.ButtonC1.Click += new System.EventHandler(this.ButtonC1_Click);
            // 
            // ButtonC2
            // 
            this.ButtonC2.Anchor = System.Windows.Forms.AnchorStyles.Bottom;
            this.ButtonC2.Cursor = System.Windows.Forms.Cursors.Hand;
            this.ButtonC2.Location = new System.Drawing.Point(260, 632);
            this.ButtonC2.Name = "ButtonC2";
            this.ButtonC2.Size = new System.Drawing.Size(105, 90);
            this.ButtonC2.TabIndex = 4;
            this.ButtonC2.Text = "Camera 2: Front: General";
            this.ButtonC2.UseVisualStyleBackColor = true;
            this.ButtonC2.Click += new System.EventHandler(this.ButtonC2_Click);
            // 
            // ButtonC3
            // 
            this.ButtonC3.Anchor = System.Windows.Forms.AnchorStyles.Bottom;
            this.ButtonC3.Cursor = System.Windows.Forms.Cursors.Hand;
            this.ButtonC3.Location = new System.Drawing.Point(389, 632);
            this.ButtonC3.Name = "ButtonC3";
            this.ButtonC3.Size = new System.Drawing.Size(105, 90);
            this.ButtonC3.TabIndex = 3;
            this.ButtonC3.Text = "Camera 3: Gear delivery";
            this.ButtonC3.UseVisualStyleBackColor = true;
            this.ButtonC3.Click += new System.EventHandler(this.ButtonC3_Click);
            // 
            // ButtonC0
            // 
            this.ButtonC0.Anchor = System.Windows.Forms.AnchorStyles.Bottom;
            this.ButtonC0.Cursor = System.Windows.Forms.Cursors.Hand;
            this.ButtonC0.Location = new System.Drawing.Point(2, 632);
            this.ButtonC0.Name = "ButtonC0";
            this.ButtonC0.Size = new System.Drawing.Size(105, 90);
            this.ButtonC0.TabIndex = 2;
            this.ButtonC0.Text = "Stop display";
            this.ButtonC0.UseVisualStyleBackColor = true;
            this.ButtonC0.Click += new System.EventHandler(this.ButtonC0_Click);
            // 
            // ButtonC4
            // 
            this.ButtonC4.Anchor = System.Windows.Forms.AnchorStyles.Bottom;
            this.ButtonC4.Cursor = System.Windows.Forms.Cursors.Hand;
            this.ButtonC4.Location = new System.Drawing.Point(518, 632);
            this.ButtonC4.Name = "ButtonC4";
            this.ButtonC4.Size = new System.Drawing.Size(105, 90);
            this.ButtonC4.TabIndex = 1;
            this.ButtonC4.Text = "Camera 4: Rope Climber";
            this.ButtonC4.UseVisualStyleBackColor = true;
            this.ButtonC4.Click += new System.EventHandler(this.ButtonC4_Click);
            // 
            // PictureBox
            // 
            this.PictureBox.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.PictureBox.BackColor = System.Drawing.Color.Black;
            this.PictureBox.ErrorImage = global::VisionClient.Properties.Resources.E;
            this.PictureBox.Image = global::VisionClient.Properties.Resources.C0;
            this.PictureBox.InitialImage = global::VisionClient.Properties.Resources.E;
            this.PictureBox.Location = new System.Drawing.Point(3, 3);
            this.PictureBox.Name = "PictureBox";
            this.PictureBox.Size = new System.Drawing.Size(619, 623);
            this.PictureBox.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.PictureBox.TabIndex = 0;
            this.PictureBox.TabStop = false;
            // 
            // ButtonAimBoiler
            // 
            this.ButtonAimBoiler.Anchor = System.Windows.Forms.AnchorStyles.Bottom;
            this.ButtonAimBoiler.Cursor = System.Windows.Forms.Cursors.Hand;
            this.ButtonAimBoiler.Location = new System.Drawing.Point(4, 632);
            this.ButtonAimBoiler.Name = "ButtonAimBoiler";
            this.ButtonAimBoiler.Size = new System.Drawing.Size(190, 90);
            this.ButtonAimBoiler.TabIndex = 9;
            this.ButtonAimBoiler.Text = "AutoAim at Boiler High";
            this.ButtonAimBoiler.UseVisualStyleBackColor = true;
            this.ButtonAimBoiler.Click += new System.EventHandler(this.ButtonAimBoiler_Click);
            // 
            // ButtonAimPeg
            // 
            this.ButtonAimPeg.Anchor = System.Windows.Forms.AnchorStyles.Bottom;
            this.ButtonAimPeg.Cursor = System.Windows.Forms.Cursors.Hand;
            this.ButtonAimPeg.Location = new System.Drawing.Point(211, 632);
            this.ButtonAimPeg.Name = "ButtonAimPeg";
            this.ButtonAimPeg.Size = new System.Drawing.Size(190, 90);
            this.ButtonAimPeg.TabIndex = 8;
            this.ButtonAimPeg.Text = "AutoAim at Gear Delivery";
            this.ButtonAimPeg.UseVisualStyleBackColor = true;
            this.ButtonAimPeg.Click += new System.EventHandler(this.ButtonAimPeg_Click);
            // 
            // ButtonAimStop
            // 
            this.ButtonAimStop.Anchor = System.Windows.Forms.AnchorStyles.Bottom;
            this.ButtonAimStop.Cursor = System.Windows.Forms.Cursors.Hand;
            this.ButtonAimStop.Location = new System.Drawing.Point(418, 632);
            this.ButtonAimStop.Name = "ButtonAimStop";
            this.ButtonAimStop.Size = new System.Drawing.Size(190, 90);
            this.ButtonAimStop.TabIndex = 7;
            this.ButtonAimStop.Text = "Stop AutoAim";
            this.ButtonAimStop.UseVisualStyleBackColor = true;
            this.ButtonAimStop.Click += new System.EventHandler(this.ButtonAimStop_Click);
            // 
            // TabPageTerminal
            // 
            this.TabPageTerminal.BackColor = System.Drawing.SystemColors.ControlDarkDark;
            this.TabPageTerminal.Controls.Add(this.TextBoxTerminalInput);
            this.TabPageTerminal.Controls.Add(this.TextBoxTerminal);
            this.TabPageTerminal.Location = new System.Drawing.Point(4, 22);
            this.TabPageTerminal.Name = "TabPageTerminal";
            this.TabPageTerminal.Padding = new System.Windows.Forms.Padding(3);
            this.TabPageTerminal.Size = new System.Drawing.Size(1256, 735);
            this.TabPageTerminal.TabIndex = 1;
            this.TabPageTerminal.Text = "Terminal";
            // 
            // TextBoxTerminalInput
            // 
            this.TextBoxTerminalInput.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.TextBoxTerminalInput.BackColor = System.Drawing.Color.Black;
            this.TextBoxTerminalInput.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.TextBoxTerminalInput.Font = new System.Drawing.Font("Consolas", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.TextBoxTerminalInput.ForeColor = System.Drawing.Color.White;
            this.TextBoxTerminalInput.Location = new System.Drawing.Point(0, 722);
            this.TextBoxTerminalInput.Name = "TextBoxTerminalInput";
            this.TextBoxTerminalInput.ScrollBars = System.Windows.Forms.ScrollBars.Both;
            this.TextBoxTerminalInput.Size = new System.Drawing.Size(1256, 13);
            this.TextBoxTerminalInput.TabIndex = 1;
            this.TextBoxTerminalInput.KeyDown += new System.Windows.Forms.KeyEventHandler(this.TextBoxTerminalInput_KeyDown);
            // 
            // TextBoxTerminal
            // 
            this.TextBoxTerminal.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.TextBoxTerminal.BackColor = System.Drawing.Color.Black;
            this.TextBoxTerminal.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.TextBoxTerminal.Font = new System.Drawing.Font("Consolas", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.TextBoxTerminal.ForeColor = System.Drawing.Color.White;
            this.TextBoxTerminal.Location = new System.Drawing.Point(0, 0);
            this.TextBoxTerminal.Multiline = true;
            this.TextBoxTerminal.Name = "TextBoxTerminal";
            this.TextBoxTerminal.ReadOnly = true;
            this.TextBoxTerminal.ScrollBars = System.Windows.Forms.ScrollBars.Both;
            this.TextBoxTerminal.Size = new System.Drawing.Size(1256, 720);
            this.TextBoxTerminal.TabIndex = 0;
            this.TextBoxTerminal.Enter += new System.EventHandler(this.TextBoxTerminal_Enter);
            // 
            // TabPageSettings
            // 
            this.TabPageSettings.Controls.Add(this.LabelControllerCameraKeys);
            this.TabPageSettings.Controls.Add(this.TextBoxIP);
            this.TabPageSettings.Controls.Add(this.LabelServerIP);
            this.TabPageSettings.Location = new System.Drawing.Point(4, 22);
            this.TabPageSettings.Name = "TabPageSettings";
            this.TabPageSettings.Size = new System.Drawing.Size(1256, 735);
            this.TabPageSettings.TabIndex = 2;
            this.TabPageSettings.Text = "Settings";
            this.TabPageSettings.UseVisualStyleBackColor = true;
            // 
            // LabelControllerCameraKeys
            // 
            this.LabelControllerCameraKeys.AutoSize = true;
            this.LabelControllerCameraKeys.Location = new System.Drawing.Point(8, 31);
            this.LabelControllerCameraKeys.Name = "LabelControllerCameraKeys";
            this.LabelControllerCameraKeys.Size = new System.Drawing.Size(201, 13);
            this.LabelControllerCameraKeys.TabIndex = 2;
            this.LabelControllerCameraKeys.Text = "Controller button to change camera view:";
            // 
            // TextBoxIP
            // 
            this.TextBoxIP.Location = new System.Drawing.Point(134, 8);
            this.TextBoxIP.MaxLength = 16;
            this.TextBoxIP.Name = "TextBoxIP";
            this.TextBoxIP.Size = new System.Drawing.Size(173, 20);
            this.TextBoxIP.TabIndex = 1;
            this.TextBoxIP.TextChanged += new System.EventHandler(this.TextBoxIP_TextChanged);
            // 
            // LabelServerIP
            // 
            this.LabelServerIP.AutoSize = true;
            this.LabelServerIP.Location = new System.Drawing.Point(8, 11);
            this.LabelServerIP.Name = "LabelServerIP";
            this.LabelServerIP.Size = new System.Drawing.Size(120, 13);
            this.LabelServerIP.TabIndex = 0;
            this.LabelServerIP.Text = "Server IP to connect to:";
            // 
            // TabPageAbout
            // 
            this.TabPageAbout.Controls.Add(this.LinkLabelCheckConnection);
            this.TabPageAbout.Controls.Add(this.LabelStatus);
            this.TabPageAbout.Location = new System.Drawing.Point(4, 22);
            this.TabPageAbout.Name = "TabPageAbout";
            this.TabPageAbout.Size = new System.Drawing.Size(1256, 735);
            this.TabPageAbout.TabIndex = 3;
            this.TabPageAbout.Text = "About";
            this.TabPageAbout.UseVisualStyleBackColor = true;
            // 
            // LinkLabelCheckConnection
            // 
            this.LinkLabelCheckConnection.AutoSize = true;
            this.LinkLabelCheckConnection.Location = new System.Drawing.Point(195, 11);
            this.LinkLabelCheckConnection.Name = "LinkLabelCheckConnection";
            this.LinkLabelCheckConnection.Size = new System.Drawing.Size(170, 13);
            this.LinkLabelCheckConnection.TabIndex = 5;
            this.LinkLabelCheckConnection.TabStop = true;
            this.LinkLabelCheckConnection.Text = "(Click here to recheck connection)";
            // 
            // LabelStatus
            // 
            this.LabelStatus.AutoSize = true;
            this.LabelStatus.Location = new System.Drawing.Point(8, 11);
            this.LabelStatus.Name = "LabelStatus";
            this.LabelStatus.Size = new System.Drawing.Size(181, 13);
            this.LabelStatus.TabIndex = 4;
            this.LabelStatus.Text = "Current connection status: OFFLINE.";
            // 
            // RefreshTimer
            // 
            this.RefreshTimer.Interval = 33;
            // 
            // ConnectionTimer
            // 
            this.ConnectionTimer.Interval = 10000;
            // 
            // PictureBoxFieldOverview
            // 
            this.PictureBoxFieldOverview.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.PictureBoxFieldOverview.BackColor = System.Drawing.SystemColors.Control;
            this.PictureBoxFieldOverview.Location = new System.Drawing.Point(42, 25);
            this.PictureBoxFieldOverview.Name = "PictureBoxFieldOverview";
            this.PictureBoxFieldOverview.Size = new System.Drawing.Size(540, 270);
            this.PictureBoxFieldOverview.TabIndex = 10;
            this.PictureBoxFieldOverview.TabStop = false;
            // 
            // FormMain
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.Control;
            this.ClientSize = new System.Drawing.Size(1264, 761);
            this.Controls.Add(this.TabControl);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MinimumSize = new System.Drawing.Size(1280, 800);
            this.Name = "FormMain";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "VisionSystem Client";
            this.FormClosed += new System.Windows.Forms.FormClosedEventHandler(this.FormMain_FormClosed);
            this.Shown += new System.EventHandler(this.FormMain_Shown);
            this.TabControl.ResumeLayout(false);
            this.TabPageDisplay.ResumeLayout(false);
            this.SplitContainer.Panel1.ResumeLayout(false);
            this.SplitContainer.Panel1.PerformLayout();
            this.SplitContainer.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.SplitContainer)).EndInit();
            this.SplitContainer.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.PictureBox)).EndInit();
            this.TabPageTerminal.ResumeLayout(false);
            this.TabPageTerminal.PerformLayout();
            this.TabPageSettings.ResumeLayout(false);
            this.TabPageSettings.PerformLayout();
            this.TabPageAbout.ResumeLayout(false);
            this.TabPageAbout.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.PictureBoxFieldOverview)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.TabControl TabControl;
        private System.Windows.Forms.TabPage TabPageDisplay;
        private System.Windows.Forms.TabPage TabPageTerminal;
        private System.Windows.Forms.SplitContainer SplitContainer;
        private System.Windows.Forms.TextBox TextBoxTerminal;
        private System.Windows.Forms.TabPage TabPageSettings;
        private System.Windows.Forms.TabPage TabPageAbout;
        private System.Windows.Forms.TextBox TextBoxTerminalInput;
        private System.Windows.Forms.PictureBox PictureBox;
        private System.Windows.Forms.Button ButtonC4;
        private System.Windows.Forms.Button ButtonC1;
        private System.Windows.Forms.Button ButtonC2;
        private System.Windows.Forms.Button ButtonC3;
        private System.Windows.Forms.Button ButtonC0;
        private System.Windows.Forms.TextBox TextBoxIP;
        private System.Windows.Forms.Label LabelServerIP;
        private System.Windows.Forms.Timer RefreshTimer;
        private System.Windows.Forms.Timer ConnectionTimer;
        private System.Windows.Forms.LinkLabel LinkLabelCheckConnection;
        private System.Windows.Forms.Label LabelStatus;
        private System.Windows.Forms.Label LabelCamera;
        private System.Windows.Forms.Label LabelControllerCameraKeys;
        private System.Windows.Forms.Button ButtonAimBoiler;
        private System.Windows.Forms.Button ButtonAimPeg;
        private System.Windows.Forms.Button ButtonAimStop;
        private System.Windows.Forms.PictureBox PictureBoxFieldOverview;
    }
}

