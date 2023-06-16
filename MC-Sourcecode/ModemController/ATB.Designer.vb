<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class F_Settings
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
        Me.TB1 = New System.Windows.Forms.TextBox
        Me.TB2 = New System.Windows.Forms.TextBox
        Me.TB3 = New System.Windows.Forms.TextBox
        Me.TB4 = New System.Windows.Forms.TextBox
        Me.TB5 = New System.Windows.Forms.TextBox
        Me.TB6 = New System.Windows.Forms.TextBox
        Me.TB7 = New System.Windows.Forms.TextBox
        Me.TB8 = New System.Windows.Forms.TextBox
        Me.L_Datei = New System.Windows.Forms.Label
        Me.BTN_Cancel = New System.Windows.Forms.Button
        Me.BTN_Save = New System.Windows.Forms.Button
        Me.Label10 = New System.Windows.Forms.Label
        Me.Label9 = New System.Windows.Forms.Label
        Me.Label8 = New System.Windows.Forms.Label
        Me.Label7 = New System.Windows.Forms.Label
        Me.Label6 = New System.Windows.Forms.Label
        Me.Label5 = New System.Windows.Forms.Label
        Me.Label4 = New System.Windows.Forms.Label
        Me.Label3 = New System.Windows.Forms.Label
        Me.Label2 = New System.Windows.Forms.Label
        Me.Label1 = New System.Windows.Forms.Label
        Me.SaveFileDialog1 = New System.Windows.Forms.SaveFileDialog
        Me.SuspendLayout()
        '
        'TB1
        '
        Me.TB1.Location = New System.Drawing.Point(86, 47)
        Me.TB1.Name = "TB1"
        Me.TB1.Size = New System.Drawing.Size(363, 20)
        Me.TB1.TabIndex = 15
        '
        'TB2
        '
        Me.TB2.Location = New System.Drawing.Point(86, 75)
        Me.TB2.Name = "TB2"
        Me.TB2.Size = New System.Drawing.Size(363, 20)
        Me.TB2.TabIndex = 16
        '
        'TB3
        '
        Me.TB3.Location = New System.Drawing.Point(86, 103)
        Me.TB3.Name = "TB3"
        Me.TB3.Size = New System.Drawing.Size(363, 20)
        Me.TB3.TabIndex = 17
        '
        'TB4
        '
        Me.TB4.Location = New System.Drawing.Point(86, 131)
        Me.TB4.Name = "TB4"
        Me.TB4.Size = New System.Drawing.Size(363, 20)
        Me.TB4.TabIndex = 20
        '
        'TB5
        '
        Me.TB5.Location = New System.Drawing.Point(86, 159)
        Me.TB5.Name = "TB5"
        Me.TB5.Size = New System.Drawing.Size(363, 20)
        Me.TB5.TabIndex = 21
        '
        'TB6
        '
        Me.TB6.Location = New System.Drawing.Point(86, 187)
        Me.TB6.Name = "TB6"
        Me.TB6.Size = New System.Drawing.Size(363, 20)
        Me.TB6.TabIndex = 25
        '
        'TB7
        '
        Me.TB7.Location = New System.Drawing.Point(86, 215)
        Me.TB7.Name = "TB7"
        Me.TB7.Size = New System.Drawing.Size(363, 20)
        Me.TB7.TabIndex = 27
        '
        'TB8
        '
        Me.TB8.Location = New System.Drawing.Point(86, 243)
        Me.TB8.Name = "TB8"
        Me.TB8.Size = New System.Drawing.Size(363, 20)
        Me.TB8.TabIndex = 29
        '
        'L_Datei
        '
        Me.L_Datei.AutoSize = True
        Me.L_Datei.ImeMode = System.Windows.Forms.ImeMode.NoControl
        Me.L_Datei.Location = New System.Drawing.Point(422, 14)
        Me.L_Datei.Name = "L_Datei"
        Me.L_Datei.Size = New System.Drawing.Size(27, 13)
        Me.L_Datei.TabIndex = 35
        Me.L_Datei.Text = "Neu"
        '
        'BTN_Cancel
        '
        Me.BTN_Cancel.ImeMode = System.Windows.Forms.ImeMode.NoControl
        Me.BTN_Cancel.Location = New System.Drawing.Point(98, 327)
        Me.BTN_Cancel.Name = "BTN_Cancel"
        Me.BTN_Cancel.Size = New System.Drawing.Size(75, 23)
        Me.BTN_Cancel.TabIndex = 32
        Me.BTN_Cancel.Text = "Abbrechen"
        Me.BTN_Cancel.UseVisualStyleBackColor = True
        '
        'BTN_Save
        '
        Me.BTN_Save.ImeMode = System.Windows.Forms.ImeMode.NoControl
        Me.BTN_Save.Location = New System.Drawing.Point(363, 327)
        Me.BTN_Save.Name = "BTN_Save"
        Me.BTN_Save.Size = New System.Drawing.Size(75, 23)
        Me.BTN_Save.TabIndex = 30
        Me.BTN_Save.Text = "Speichern"
        Me.BTN_Save.UseVisualStyleBackColor = True
        '
        'Label10
        '
        Me.Label10.AutoSize = True
        Me.Label10.ImeMode = System.Windows.Forms.ImeMode.NoControl
        Me.Label10.Location = New System.Drawing.Point(92, 285)
        Me.Label10.Name = "Label10"
        Me.Label10.Size = New System.Drawing.Size(346, 13)
        Me.Label10.TabIndex = 22
        Me.Label10.Text = "Es können auch mehrere AT-Befehle in einer Zeile Geschrieben werden"
        '
        'Label9
        '
        Me.Label9.AutoSize = True
        Me.Label9.ImeMode = System.Windows.Forms.ImeMode.NoControl
        Me.Label9.Location = New System.Drawing.Point(50, 106)
        Me.Label9.Name = "Label9"
        Me.Label9.Size = New System.Drawing.Size(21, 13)
        Me.Label9.TabIndex = 34
        Me.Label9.Text = "AT"
        '
        'Label8
        '
        Me.Label8.AutoSize = True
        Me.Label8.ImeMode = System.Windows.Forms.ImeMode.NoControl
        Me.Label8.Location = New System.Drawing.Point(50, 162)
        Me.Label8.Name = "Label8"
        Me.Label8.Size = New System.Drawing.Size(21, 13)
        Me.Label8.TabIndex = 33
        Me.Label8.Text = "AT"
        '
        'Label7
        '
        Me.Label7.AutoSize = True
        Me.Label7.ImeMode = System.Windows.Forms.ImeMode.NoControl
        Me.Label7.Location = New System.Drawing.Point(50, 246)
        Me.Label7.Name = "Label7"
        Me.Label7.Size = New System.Drawing.Size(21, 13)
        Me.Label7.TabIndex = 31
        Me.Label7.Text = "AT"
        '
        'Label6
        '
        Me.Label6.AutoSize = True
        Me.Label6.ImeMode = System.Windows.Forms.ImeMode.NoControl
        Me.Label6.Location = New System.Drawing.Point(50, 218)
        Me.Label6.Name = "Label6"
        Me.Label6.Size = New System.Drawing.Size(21, 13)
        Me.Label6.TabIndex = 28
        Me.Label6.Text = "AT"
        '
        'Label5
        '
        Me.Label5.AutoSize = True
        Me.Label5.ImeMode = System.Windows.Forms.ImeMode.NoControl
        Me.Label5.Location = New System.Drawing.Point(50, 78)
        Me.Label5.Name = "Label5"
        Me.Label5.Size = New System.Drawing.Size(21, 13)
        Me.Label5.TabIndex = 26
        Me.Label5.Text = "AT"
        '
        'Label4
        '
        Me.Label4.AutoSize = True
        Me.Label4.ImeMode = System.Windows.Forms.ImeMode.NoControl
        Me.Label4.Location = New System.Drawing.Point(50, 50)
        Me.Label4.Name = "Label4"
        Me.Label4.Size = New System.Drawing.Size(21, 13)
        Me.Label4.TabIndex = 24
        Me.Label4.Text = "AT"
        '
        'Label3
        '
        Me.Label3.AutoSize = True
        Me.Label3.ImeMode = System.Windows.Forms.ImeMode.NoControl
        Me.Label3.Location = New System.Drawing.Point(50, 134)
        Me.Label3.Name = "Label3"
        Me.Label3.Size = New System.Drawing.Size(21, 13)
        Me.Label3.TabIndex = 23
        Me.Label3.Text = "AT"
        '
        'Label2
        '
        Me.Label2.AutoSize = True
        Me.Label2.ImeMode = System.Windows.Forms.ImeMode.NoControl
        Me.Label2.Location = New System.Drawing.Point(50, 190)
        Me.Label2.Name = "Label2"
        Me.Label2.Size = New System.Drawing.Size(21, 13)
        Me.Label2.TabIndex = 19
        Me.Label2.Text = "AT"
        '
        'Label1
        '
        Me.Label1.AutoSize = True
        Me.Label1.Font = New System.Drawing.Font("Microsoft Sans Serif", 12.0!, System.Drawing.FontStyle.Bold)
        Me.Label1.ImeMode = System.Windows.Forms.ImeMode.NoControl
        Me.Label1.Location = New System.Drawing.Point(12, 9)
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(118, 20)
        Me.Label1.TabIndex = 18
        Me.Label1.Text = "Einstellungen"
        '
        'F_Settings
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(480, 366)
        Me.Controls.Add(Me.TB1)
        Me.Controls.Add(Me.TB2)
        Me.Controls.Add(Me.TB3)
        Me.Controls.Add(Me.TB4)
        Me.Controls.Add(Me.TB5)
        Me.Controls.Add(Me.TB6)
        Me.Controls.Add(Me.TB7)
        Me.Controls.Add(Me.TB8)
        Me.Controls.Add(Me.L_Datei)
        Me.Controls.Add(Me.BTN_Cancel)
        Me.Controls.Add(Me.BTN_Save)
        Me.Controls.Add(Me.Label10)
        Me.Controls.Add(Me.Label9)
        Me.Controls.Add(Me.Label8)
        Me.Controls.Add(Me.Label7)
        Me.Controls.Add(Me.Label6)
        Me.Controls.Add(Me.Label5)
        Me.Controls.Add(Me.Label4)
        Me.Controls.Add(Me.Label3)
        Me.Controls.Add(Me.Label2)
        Me.Controls.Add(Me.Label1)
        Me.DataBindings.Add(New System.Windows.Forms.Binding("Location", Global.ModemController.My.MySettings.Default, "ATB_LocationXY", True, System.Windows.Forms.DataSourceUpdateMode.OnPropertyChanged))
        Me.Location = Global.ModemController.My.MySettings.Default.ATB_LocationXY
        Me.Name = "F_Settings"
        Me.Text = "ATB"
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub
    Friend WithEvents TB1 As System.Windows.Forms.TextBox
    Friend WithEvents TB2 As System.Windows.Forms.TextBox
    Friend WithEvents TB3 As System.Windows.Forms.TextBox
    Friend WithEvents TB4 As System.Windows.Forms.TextBox
    Friend WithEvents TB5 As System.Windows.Forms.TextBox
    Friend WithEvents TB6 As System.Windows.Forms.TextBox
    Friend WithEvents TB7 As System.Windows.Forms.TextBox
    Friend WithEvents TB8 As System.Windows.Forms.TextBox
    Friend WithEvents L_Datei As System.Windows.Forms.Label
    Friend WithEvents BTN_Cancel As System.Windows.Forms.Button
    Friend WithEvents BTN_Save As System.Windows.Forms.Button
    Friend WithEvents Label10 As System.Windows.Forms.Label
    Friend WithEvents Label9 As System.Windows.Forms.Label
    Friend WithEvents Label8 As System.Windows.Forms.Label
    Friend WithEvents Label7 As System.Windows.Forms.Label
    Friend WithEvents Label6 As System.Windows.Forms.Label
    Friend WithEvents Label5 As System.Windows.Forms.Label
    Friend WithEvents Label4 As System.Windows.Forms.Label
    Friend WithEvents Label3 As System.Windows.Forms.Label
    Friend WithEvents Label2 As System.Windows.Forms.Label
    Friend WithEvents Label1 As System.Windows.Forms.Label
    Friend WithEvents SaveFileDialog1 As System.Windows.Forms.SaveFileDialog
End Class
