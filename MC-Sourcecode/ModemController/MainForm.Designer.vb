<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class MainForm
    Inherits System.Windows.Forms.Form

    'Das Formular überschreibt den Löschvorgang, um die Komponentenliste zu bereinigen.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Wird vom Windows Form-Designer benötigt.
    Private components As System.ComponentModel.IContainer

    'Hinweis: Die folgende Prozedur ist für den Windows Form-Designer erforderlich.
    'Das Bearbeiten ist mit dem Windows Form-Designer möglich.  
    'Das Bearbeiten mit dem Code-Editor ist nicht möglich.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.components = New System.ComponentModel.Container()
        Me.Label2 = New System.Windows.Forms.Label()
        Me.Label9 = New System.Windows.Forms.Label()
        Me.Label6 = New System.Windows.Forms.Label()
        Me.Label1 = New System.Windows.Forms.Label()
        Me.TXT_Antwort = New System.Windows.Forms.TextBox()
        Me.T_ATBefehl = New System.Windows.Forms.TextBox()
        Me.T_MSN = New System.Windows.Forms.TextBox()
        Me.BTN_CLS = New System.Windows.Forms.Button()
        Me.BTN_OpenPort = New System.Windows.Forms.Button()
        Me.BTN_ClosePort = New System.Windows.Forms.Button()
        Me.Btn_Senden = New System.Windows.Forms.Button()
        Me.Pnl_PCSite = New System.Windows.Forms.Panel()
        Me.Label3 = New System.Windows.Forms.Label()
        Me.C_HandShake = New System.Windows.Forms.ComboBox()
        Me.Label7 = New System.Windows.Forms.Label()
        Me.C_Parity = New System.Windows.Forms.ComboBox()
        Me.Label8 = New System.Windows.Forms.Label()
        Me.C_Stoppbits = New System.Windows.Forms.ComboBox()
        Me.Label5 = New System.Windows.Forms.Label()
        Me.C_Bits = New System.Windows.Forms.ComboBox()
        Me.Label4 = New System.Windows.Forms.Label()
        Me.C_Speed = New System.Windows.Forms.ComboBox()
        Me.Label10 = New System.Windows.Forms.Label()
        Me.C_Comport = New System.Windows.Forms.ComboBox()
        Me.SerialPort1 = New System.IO.Ports.SerialPort(Me.components)
        Me.Btn_Exit = New System.Windows.Forms.Button()
        Me.CB_Senden = New System.Windows.Forms.CheckBox()
        Me.FontDialog1 = New System.Windows.Forms.FontDialog()
        Me.TreeView1 = New System.Windows.Forms.TreeView()
        Me.Btn_NewSubNode = New System.Windows.Forms.Button()
        Me.BTN_NewDescr = New System.Windows.Forms.Button()
        Me.BTN_DelNode = New System.Windows.Forms.Button()
        Me.Btn_NewNode = New System.Windows.Forms.Button()
        Me.ToolTip1 = New System.Windows.Forms.ToolTip(Me.components)
        Me.Pnl_PCSite.SuspendLayout()
        Me.SuspendLayout()
        '
        'Label2
        '
        Me.Label2.AutoSize = True
        Me.Label2.Location = New System.Drawing.Point(381, 54)
        Me.Label2.Name = "Label2"
        Me.Label2.Size = New System.Drawing.Size(34, 13)
        Me.Label2.TabIndex = 20
        Me.Label2.Text = "MSN:"
        '
        'Label9
        '
        Me.Label9.AutoSize = True
        Me.Label9.Location = New System.Drawing.Point(285, 182)
        Me.Label9.Name = "Label9"
        Me.Label9.Size = New System.Drawing.Size(43, 13)
        Me.Label9.TabIndex = 19
        Me.Label9.Text = "Antwort"
        '
        'Label6
        '
        Me.Label6.AutoSize = True
        Me.Label6.Location = New System.Drawing.Point(285, 93)
        Me.Label6.Name = "Label6"
        Me.Label6.Size = New System.Drawing.Size(60, 13)
        Me.Label6.TabIndex = 18
        Me.Label6.Text = "AT-Befehle"
        '
        'Label1
        '
        Me.Label1.AutoSize = True
        Me.Label1.Font = New System.Drawing.Font("Microsoft Sans Serif", 20.0!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.Label1.Location = New System.Drawing.Point(12, 6)
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(252, 31)
        Me.Label1.TabIndex = 17
        Me.Label1.Text = "Modem Controller "
        '
        'TXT_Antwort
        '
        Me.TXT_Antwort.AcceptsReturn = True
        Me.TXT_Antwort.Anchor = CType((((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Bottom) _
            Or System.Windows.Forms.AnchorStyles.Left) _
            Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.TXT_Antwort.DataBindings.Add(New System.Windows.Forms.Binding("Font", Global.ModemController.My.MySettings.Default, "TxtAnwFont", True, System.Windows.Forms.DataSourceUpdateMode.OnPropertyChanged))
        Me.TXT_Antwort.Font = Global.ModemController.My.MySettings.Default.TxtAnwFont
        Me.TXT_Antwort.Location = New System.Drawing.Point(288, 160)
        Me.TXT_Antwort.Multiline = True
        Me.TXT_Antwort.Name = "TXT_Antwort"
        Me.TXT_Antwort.ScrollBars = System.Windows.Forms.ScrollBars.Both
        Me.TXT_Antwort.Size = New System.Drawing.Size(536, 484)
        Me.TXT_Antwort.TabIndex = 22
        '
        'T_ATBefehl
        '
        Me.T_ATBefehl.Location = New System.Drawing.Point(351, 90)
        Me.T_ATBefehl.Name = "T_ATBefehl"
        Me.T_ATBefehl.Size = New System.Drawing.Size(467, 20)
        Me.T_ATBefehl.TabIndex = 23
        '
        'T_MSN
        '
        Me.T_MSN.Location = New System.Drawing.Point(418, 50)
        Me.T_MSN.Name = "T_MSN"
        Me.T_MSN.Size = New System.Drawing.Size(400, 20)
        Me.T_MSN.TabIndex = 24
        '
        'BTN_CLS
        '
        Me.BTN_CLS.Location = New System.Drawing.Point(290, 116)
        Me.BTN_CLS.Name = "BTN_CLS"
        Me.BTN_CLS.Size = New System.Drawing.Size(38, 38)
        Me.BTN_CLS.TabIndex = 31
        Me.BTN_CLS.UseVisualStyleBackColor = True
        '
        'BTN_OpenPort
        '
        Me.BTN_OpenPort.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Zoom
        Me.BTN_OpenPort.Location = New System.Drawing.Point(647, 116)
        Me.BTN_OpenPort.Name = "BTN_OpenPort"
        Me.BTN_OpenPort.Size = New System.Drawing.Size(38, 38)
        Me.BTN_OpenPort.TabIndex = 30
        Me.BTN_OpenPort.UseVisualStyleBackColor = True
        '
        'BTN_ClosePort
        '
        Me.BTN_ClosePort.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Zoom
        Me.BTN_ClosePort.Location = New System.Drawing.Point(709, 116)
        Me.BTN_ClosePort.Name = "BTN_ClosePort"
        Me.BTN_ClosePort.RightToLeft = System.Windows.Forms.RightToLeft.Yes
        Me.BTN_ClosePort.Size = New System.Drawing.Size(38, 38)
        Me.BTN_ClosePort.TabIndex = 29
        Me.BTN_ClosePort.UseVisualStyleBackColor = True
        '
        'Btn_Senden
        '
        Me.Btn_Senden.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Zoom
        Me.Btn_Senden.Location = New System.Drawing.Point(780, 116)
        Me.Btn_Senden.Name = "Btn_Senden"
        Me.Btn_Senden.Size = New System.Drawing.Size(38, 38)
        Me.Btn_Senden.TabIndex = 28
        Me.Btn_Senden.UseVisualStyleBackColor = True
        '
        'Pnl_PCSite
        '
        Me.Pnl_PCSite.Anchor = CType((System.Windows.Forms.AnchorStyles.Bottom Or System.Windows.Forms.AnchorStyles.Left), System.Windows.Forms.AnchorStyles)
        Me.Pnl_PCSite.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        Me.Pnl_PCSite.Controls.Add(Me.Label3)
        Me.Pnl_PCSite.Controls.Add(Me.C_HandShake)
        Me.Pnl_PCSite.Controls.Add(Me.Label7)
        Me.Pnl_PCSite.Controls.Add(Me.C_Parity)
        Me.Pnl_PCSite.Controls.Add(Me.Label8)
        Me.Pnl_PCSite.Controls.Add(Me.C_Stoppbits)
        Me.Pnl_PCSite.Controls.Add(Me.Label5)
        Me.Pnl_PCSite.Controls.Add(Me.C_Bits)
        Me.Pnl_PCSite.Controls.Add(Me.Label4)
        Me.Pnl_PCSite.Controls.Add(Me.C_Speed)
        Me.Pnl_PCSite.Controls.Add(Me.Label10)
        Me.Pnl_PCSite.Controls.Add(Me.C_Comport)
        Me.Pnl_PCSite.Location = New System.Drawing.Point(19, 466)
        Me.Pnl_PCSite.Name = "Pnl_PCSite"
        Me.Pnl_PCSite.Size = New System.Drawing.Size(230, 178)
        Me.Pnl_PCSite.TabIndex = 33
        Me.Pnl_PCSite.Tag = ""
        '
        'Label3
        '
        Me.Label3.AutoSize = True
        Me.Label3.Font = New System.Drawing.Font("Microsoft Sans Serif", 8.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.Label3.Location = New System.Drawing.Point(6, 145)
        Me.Label3.Name = "Label3"
        Me.Label3.Size = New System.Drawing.Size(68, 13)
        Me.Label3.TabIndex = 11
        Me.Label3.Text = "Handschake"
        '
        'C_HandShake
        '
        Me.C_HandShake.FormattingEnabled = True
        Me.C_HandShake.Location = New System.Drawing.Point(107, 141)
        Me.C_HandShake.Name = "C_HandShake"
        Me.C_HandShake.Size = New System.Drawing.Size(106, 21)
        Me.C_HandShake.TabIndex = 10
        Me.C_HandShake.Tag = System.IO.Ports.Handshake.None
        '
        'Label7
        '
        Me.Label7.AutoSize = True
        Me.Label7.Font = New System.Drawing.Font("Microsoft Sans Serif", 8.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.Label7.Location = New System.Drawing.Point(6, 118)
        Me.Label7.Name = "Label7"
        Me.Label7.Size = New System.Drawing.Size(33, 13)
        Me.Label7.TabIndex = 9
        Me.Label7.Text = "Parity"
        '
        'C_Parity
        '
        Me.C_Parity.FormattingEnabled = True
        Me.C_Parity.Location = New System.Drawing.Point(107, 114)
        Me.C_Parity.Name = "C_Parity"
        Me.C_Parity.Size = New System.Drawing.Size(106, 21)
        Me.C_Parity.TabIndex = 8
        Me.C_Parity.Tag = System.IO.Ports.Parity.None
        '
        'Label8
        '
        Me.Label8.AutoSize = True
        Me.Label8.Font = New System.Drawing.Font("Microsoft Sans Serif", 8.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.Label8.Location = New System.Drawing.Point(6, 91)
        Me.Label8.Name = "Label8"
        Me.Label8.Size = New System.Drawing.Size(35, 13)
        Me.Label8.TabIndex = 7
        Me.Label8.Text = "Stopp"
        '
        'C_Stoppbits
        '
        Me.C_Stoppbits.FormattingEnabled = True
        Me.C_Stoppbits.Location = New System.Drawing.Point(107, 87)
        Me.C_Stoppbits.Name = "C_Stoppbits"
        Me.C_Stoppbits.Size = New System.Drawing.Size(106, 21)
        Me.C_Stoppbits.TabIndex = 6
        Me.C_Stoppbits.Tag = 1
        '
        'Label5
        '
        Me.Label5.AutoSize = True
        Me.Label5.Font = New System.Drawing.Font("Microsoft Sans Serif", 8.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.Label5.Location = New System.Drawing.Point(6, 64)
        Me.Label5.Name = "Label5"
        Me.Label5.Size = New System.Drawing.Size(19, 13)
        Me.Label5.TabIndex = 5
        Me.Label5.Text = "Bit"
        '
        'C_Bits
        '
        Me.C_Bits.FormattingEnabled = True
        Me.C_Bits.Location = New System.Drawing.Point(107, 60)
        Me.C_Bits.Name = "C_Bits"
        Me.C_Bits.Size = New System.Drawing.Size(106, 21)
        Me.C_Bits.TabIndex = 4
        Me.C_Bits.Tag = 8
        '
        'Label4
        '
        Me.Label4.AutoSize = True
        Me.Label4.Font = New System.Drawing.Font("Microsoft Sans Serif", 8.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.Label4.Location = New System.Drawing.Point(6, 37)
        Me.Label4.Name = "Label4"
        Me.Label4.Size = New System.Drawing.Size(38, 13)
        Me.Label4.TabIndex = 3
        Me.Label4.Text = "Speed"
        '
        'C_Speed
        '
        Me.C_Speed.FormattingEnabled = True
        Me.C_Speed.Location = New System.Drawing.Point(107, 33)
        Me.C_Speed.Name = "C_Speed"
        Me.C_Speed.Size = New System.Drawing.Size(106, 21)
        Me.C_Speed.TabIndex = 2
        Me.C_Speed.Tag = Global.ModemController.My.MySettings.Default.Speed
        '
        'Label10
        '
        Me.Label10.AutoSize = True
        Me.Label10.Font = New System.Drawing.Font("Microsoft Sans Serif", 8.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.Label10.Location = New System.Drawing.Point(6, 10)
        Me.Label10.Name = "Label10"
        Me.Label10.Size = New System.Drawing.Size(50, 13)
        Me.Label10.TabIndex = 1
        Me.Label10.Text = "Com-Port"
        '
        'C_Comport
        '
        Me.C_Comport.FormattingEnabled = True
        Me.C_Comport.Location = New System.Drawing.Point(107, 6)
        Me.C_Comport.Name = "C_Comport"
        Me.C_Comport.Size = New System.Drawing.Size(106, 21)
        Me.C_Comport.TabIndex = 0
        Me.C_Comport.Tag = Global.ModemController.My.MySettings.Default.Port
        '
        'Btn_Exit
        '
        Me.Btn_Exit.Anchor = CType((System.Windows.Forms.AnchorStyles.Bottom Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.Btn_Exit.Location = New System.Drawing.Point(776, 650)
        Me.Btn_Exit.Name = "Btn_Exit"
        Me.Btn_Exit.Size = New System.Drawing.Size(42, 42)
        Me.Btn_Exit.TabIndex = 34
        Me.Btn_Exit.UseVisualStyleBackColor = True
        '
        'CB_Senden
        '
        Me.CB_Senden.AutoSize = True
        Me.CB_Senden.Location = New System.Drawing.Point(288, 53)
        Me.CB_Senden.Name = "CB_Senden"
        Me.CB_Senden.Size = New System.Drawing.Size(81, 17)
        Me.CB_Senden.TabIndex = 35
        Me.CB_Senden.Text = "Senden --->"
        Me.CB_Senden.UseVisualStyleBackColor = True
        '
        'TreeView1
        '
        Me.TreeView1.Anchor = CType(((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Bottom) _
            Or System.Windows.Forms.AnchorStyles.Left), System.Windows.Forms.AnchorStyles)
        Me.TreeView1.Location = New System.Drawing.Point(18, 54)
        Me.TreeView1.Name = "TreeView1"
        Me.TreeView1.Size = New System.Drawing.Size(230, 357)
        Me.TreeView1.TabIndex = 36
        '
        'Btn_NewSubNode
        '
        Me.Btn_NewSubNode.Anchor = CType((System.Windows.Forms.AnchorStyles.Bottom Or System.Windows.Forms.AnchorStyles.Left), System.Windows.Forms.AnchorStyles)
        Me.Btn_NewSubNode.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Zoom
        Me.Btn_NewSubNode.Location = New System.Drawing.Point(88, 421)
        Me.Btn_NewSubNode.Name = "Btn_NewSubNode"
        Me.Btn_NewSubNode.Size = New System.Drawing.Size(38, 38)
        Me.Btn_NewSubNode.TabIndex = 38
        Me.Btn_NewSubNode.UseVisualStyleBackColor = True
        '
        'BTN_NewDescr
        '
        Me.BTN_NewDescr.Anchor = CType((System.Windows.Forms.AnchorStyles.Bottom Or System.Windows.Forms.AnchorStyles.Left), System.Windows.Forms.AnchorStyles)
        Me.BTN_NewDescr.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Zoom
        Me.BTN_NewDescr.Location = New System.Drawing.Point(137, 421)
        Me.BTN_NewDescr.Name = "BTN_NewDescr"
        Me.BTN_NewDescr.Size = New System.Drawing.Size(38, 38)
        Me.BTN_NewDescr.TabIndex = 39
        Me.BTN_NewDescr.UseVisualStyleBackColor = True
        '
        'BTN_DelNode
        '
        Me.BTN_DelNode.Anchor = CType((System.Windows.Forms.AnchorStyles.Bottom Or System.Windows.Forms.AnchorStyles.Left), System.Windows.Forms.AnchorStyles)
        Me.BTN_DelNode.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Zoom
        Me.BTN_DelNode.Location = New System.Drawing.Point(186, 421)
        Me.BTN_DelNode.Name = "BTN_DelNode"
        Me.BTN_DelNode.Size = New System.Drawing.Size(38, 38)
        Me.BTN_DelNode.TabIndex = 40
        Me.BTN_DelNode.UseVisualStyleBackColor = True
        '
        'Btn_NewNode
        '
        Me.Btn_NewNode.Anchor = CType((System.Windows.Forms.AnchorStyles.Bottom Or System.Windows.Forms.AnchorStyles.Left), System.Windows.Forms.AnchorStyles)
        Me.Btn_NewNode.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Zoom
        Me.Btn_NewNode.Location = New System.Drawing.Point(39, 421)
        Me.Btn_NewNode.Name = "Btn_NewNode"
        Me.Btn_NewNode.Size = New System.Drawing.Size(38, 38)
        Me.Btn_NewNode.TabIndex = 41
        Me.Btn_NewNode.UseVisualStyleBackColor = True
        '
        'MainForm
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(836, 699)
        Me.Controls.Add(Me.Btn_NewNode)
        Me.Controls.Add(Me.BTN_DelNode)
        Me.Controls.Add(Me.BTN_NewDescr)
        Me.Controls.Add(Me.Btn_NewSubNode)
        Me.Controls.Add(Me.TreeView1)
        Me.Controls.Add(Me.CB_Senden)
        Me.Controls.Add(Me.Btn_Exit)
        Me.Controls.Add(Me.Pnl_PCSite)
        Me.Controls.Add(Me.BTN_CLS)
        Me.Controls.Add(Me.BTN_OpenPort)
        Me.Controls.Add(Me.BTN_ClosePort)
        Me.Controls.Add(Me.Btn_Senden)
        Me.Controls.Add(Me.T_MSN)
        Me.Controls.Add(Me.T_ATBefehl)
        Me.Controls.Add(Me.TXT_Antwort)
        Me.Controls.Add(Me.Label2)
        Me.Controls.Add(Me.Label9)
        Me.Controls.Add(Me.Label6)
        Me.Controls.Add(Me.Label1)
        Me.DataBindings.Add(New System.Windows.Forms.Binding("Location", Global.ModemController.My.MySettings.Default, "LocationXY", True, System.Windows.Forms.DataSourceUpdateMode.OnPropertyChanged))
        Me.Location = Global.ModemController.My.MySettings.Default.LocationXY
        Me.Name = "MainForm"
        Me.Text = "Modem Controller"
        Me.Pnl_PCSite.ResumeLayout(False)
        Me.Pnl_PCSite.PerformLayout()
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub
    Friend WithEvents Label2 As System.Windows.Forms.Label
    Friend WithEvents Label9 As System.Windows.Forms.Label
    Friend WithEvents Label6 As System.Windows.Forms.Label
    Friend WithEvents Label1 As System.Windows.Forms.Label
    Friend WithEvents TXT_Antwort As System.Windows.Forms.TextBox
    Friend WithEvents T_ATBefehl As System.Windows.Forms.TextBox
    Friend WithEvents T_MSN As System.Windows.Forms.TextBox
    Friend WithEvents BTN_CLS As System.Windows.Forms.Button
    Friend WithEvents BTN_OpenPort As System.Windows.Forms.Button
    Friend WithEvents BTN_ClosePort As System.Windows.Forms.Button
    Friend WithEvents Btn_Senden As System.Windows.Forms.Button
    Friend WithEvents Pnl_PCSite As System.Windows.Forms.Panel
    Friend WithEvents Label3 As System.Windows.Forms.Label
    Friend WithEvents C_HandShake As System.Windows.Forms.ComboBox
    Friend WithEvents Label7 As System.Windows.Forms.Label
    Friend WithEvents C_Parity As System.Windows.Forms.ComboBox
    Friend WithEvents Label8 As System.Windows.Forms.Label
    Friend WithEvents C_Stoppbits As System.Windows.Forms.ComboBox
    Friend WithEvents Label5 As System.Windows.Forms.Label
    Friend WithEvents C_Bits As System.Windows.Forms.ComboBox
    Friend WithEvents Label4 As System.Windows.Forms.Label
    Friend WithEvents C_Speed As System.Windows.Forms.ComboBox
    Friend WithEvents Label10 As System.Windows.Forms.Label
    Friend WithEvents C_Comport As System.Windows.Forms.ComboBox
    Friend WithEvents SerialPort1 As System.IO.Ports.SerialPort
    Friend WithEvents Btn_Exit As System.Windows.Forms.Button
    Friend WithEvents CB_Senden As System.Windows.Forms.CheckBox
    Friend WithEvents FontDialog1 As System.Windows.Forms.FontDialog
    Friend WithEvents TreeView1 As System.Windows.Forms.TreeView
    Friend WithEvents Btn_NewSubNode As System.Windows.Forms.Button
    Friend WithEvents BTN_NewDescr As System.Windows.Forms.Button
    Friend WithEvents BTN_DelNode As System.Windows.Forms.Button
    Friend WithEvents Btn_NewNode As System.Windows.Forms.Button
    Friend WithEvents ToolTip1 As System.Windows.Forms.ToolTip

End Class
