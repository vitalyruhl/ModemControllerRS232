Imports System.IO
Imports System.IO.Ports
Imports System.Xml

Public Class MainForm

    Public MyComport1 As New SerialPort
    Dim _Continue As Boolean
    Delegate Sub SetTextCallback(ByVal [text] As String)


#Region "Programmsteuerung"

    Private Function CutOutAT(ByVal text As String, ByVal StIndex As Integer) As String
        Dim TempString As String
        Try
            TempString = ""

            For i = StIndex To text.Length - 1
                If text.Chars(i) = vbCr Then Exit For
                TempString += text.Chars(i)
            Next

            If TempString = "" Then TempString = "Leer!"

            Return TempString
        Catch ex As Exception
            MsgBox("na supper! hier ist der fehler --> SUB LadeEinstellungen: " & vbNewLine & ex.Message.ToString)
            CutOutAT = StIndex.ToString
        End Try
    End Function

    Private Sub T_ATBefehl_KeyPress(ByVal sender As System.Object, ByVal e As System.Windows.Forms.KeyPressEventArgs) Handles T_ATBefehl.KeyPress
        If e.KeyChar = vbCr Then
            Call BtnSenden()
        End If
    End Sub

    Private Sub TXT_Antwort_KeyPress(ByVal sender As System.Object, ByVal e As System.Windows.Forms.KeyPressEventArgs) Handles TXT_Antwort.KeyPress

        If e.KeyChar = vbCr Then

            If TXT_Antwort.SelectedText <> "" Then
                Clipboard.SetDataObject(TXT_Antwort.SelectedText) '=Kopieren
                TXT_Antwort.AppendText(TXT_Antwort.SelectedText)
                Dim iData As IDataObject = Clipboard.GetDataObject() 'Daten holen
                T_ATBefehl.Text = CType(iData.GetData(DataFormats.Text), String) 'Einfügen
            Else
                T_ATBefehl.Text = CutOutAT(TXT_Antwort.Text, TXT_Antwort.GetFirstCharIndexOfCurrentLine)
            End If
            Call TimeOutAbwarten()
            Call SendeATBefehl()

        End If
    End Sub

    Private Sub Btn_Exit_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Btn_Exit.Click
        Dim msg As String = "Beenden?"
        Try

            If MsgBox(msg, MsgBoxStyle.YesNo, msg) = MsgBoxResult.Yes Then
                MyComport1.Close()
                My.Settings.NodeState = (saveNodeState(TreeView1.Nodes(1)))
                My.Settings.Save()
                Me.Close()
            End If

        Catch ex As Exception 'Exception
            Me.Close()
        End Try

    End Sub

    Private Sub FrmMain_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
       
        initialisieren()
   
    End Sub

    Private Sub FrmMain_FormClosing(ByVal sender As System.Object, ByVal e As System.Windows.Forms.FormClosingEventArgs) Handles MyBase.FormClosing
        Try

            MyComport1.Close()

        Catch ex As Exception 
            MyComport1.Close()
        End Try

    End Sub

   



    Private Sub TXT_Antwort_MouseDoubleClick(ByVal sender As System.Object, ByVal e As System.Windows.Forms.MouseEventArgs) Handles TXT_Antwort.MouseDoubleClick
        Dim MyFontDialod As New FontDialog
        MyFontDialod.Font = TXT_Antwort.Font
        If MyFontDialod.ShowDialog() = DialogResult.OK Then
            TXT_Antwort.Font = MyFontDialod.Font
        End If
    End Sub


#End Region

#Region "buttons"

    Private Sub BTN_CLS_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles BTN_CLS.Click
        TXT_Antwort.Text = "Liste geleert" & vbNewLine
    End Sub


    Private Sub Btn_Senden_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Btn_Senden.Click
        Call BtnSenden()
    End Sub

#End Region

#Region "Com Steuerung"


    Private Sub SendeNummer()
        MyComport1.WriteLine("AT #Z=" & T_MSN.Text & vbNewLine)
    End Sub

    Private Sub SendeSpeichern()
        MyComport1.WriteLine("AT &W" & vbNewLine)
        Application.DoEvents()
    End Sub

    Private Sub SendeATBefehl()
        Try
            MyComport1.WriteLine(T_ATBefehl.Text & vbNewLine)
        Catch ex As InvalidOperationException
            MsgBox("na supper! hier ist der fehler --> SUB SendeATBefehl: " & vbNewLine & vbNewLine & ex.Message.ToString)
        End Try
    End Sub

    Private Sub TimeOutAbwarten()
        Dim temp As Integer
        For temp = 1 To 260000
            Application.DoEvents()
        Next
    End Sub

    Private Sub BtnSenden()

        Try

            If CB_Senden.Checked = True Then
                SendeNummer()
                TimeOutAbwarten()
                SendeSpeichern()
                TimeOutAbwarten()
            End If
            SendeATBefehl()

        Catch ex As TimeoutException
            ' do nothing
            Application.DoEvents()
            ' ADDText("Timeoutexception" & vbNewLine)
        Catch ex As System.Exception
            MsgBox("na supper! hier ist der fehler --> SUB BtnSenden: " & vbNewLine & vbNewLine & ex.Message.ToString)
            ' ADDText(ex.Message & vbNewLine)
        End Try


    End Sub


    Private Sub Antwort()

        Try

            _Continue = True
            Dim message As String




            While (_Continue)
                Try
                    Application.DoEvents()
                    message = MyComport1.ReadLine

                    ADDText(vbNewLine & message & vbNewLine)

                    TXT_Antwort.AppendText(" " & vbNewLine)
                    TXT_Antwort.ScrollToCaret()

                Catch ex As TimeoutException
                    ' Timeout Nichts tun?
                    Application.DoEvents()

                End Try

            End While


        Catch ex As Exception
            Application.DoEvents()
            ADDText(ex.Message & vbNewLine)
        End Try
    End Sub

    Private Sub ADDText(ByVal [text] As String)
        If Me.TXT_Antwort.InvokeRequired Then
            Dim d As New SetTextCallback(AddressOf ADDText)
            Me.Invoke(d, New Object() {[text]})
        Else
            Me.TXT_Antwort.Text &= [text]
        End If
    End Sub


    Private Sub BTN_OpenPort_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles BTN_OpenPort.Click
        Try

            BTN_ClosePort.Enabled = True
            BTN_OpenPort.Enabled = False
            Btn_Senden.Enabled = True
            portsetzen()

            MyComport1.Open()

            ADDText("Port Offen" & vbNewLine & vbNewLine)
            ' ADDText("Daten empfangen:" & vbNewLine)

            Antwort()

        Catch ex As Exception
            MsgBox("na Super! hier ist der Fehler --> SUB BTN_OpenPort_Click: " & vbNewLine & ex.Message.ToString)
        End Try
    End Sub

    Private Sub BTN_ClosePort_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles BTN_ClosePort.Click
        Try
            MyComport1.Close()
            TXT_Antwort.Text &= "Ports geschlossen" & vbNewLine
            BTN_ClosePort.Enabled = False
            BTN_OpenPort.Enabled = True
            Btn_Senden.Enabled = False
        Catch ex As Exception
            'nichts tuhn
            Application.DoEvents()
        End Try
    End Sub

#End Region

#Region "Com Einstellungen"

    Private Sub LadeEinstellungen(ByVal MyFileName As String)

        Dim sw As New StreamReader(My.Computer.FileSystem.CurrentDirectory.ToString & "\" & MyFileName, False)
        Dim temp As String

        Try
            T_ATBefehl.Text = "AT "

            Do
                temp = sw.ReadLine.ToString
                T_ATBefehl.Text &= temp & " "

            Loop Until temp = Nothing


        Catch ex As Exception
            MsgBox("na supper! hier ist der fehler --> SUB LadeEinstellungen: " & vbNewLine & ex.Message.ToString)
        Finally
            sw.Close()

        End Try

    End Sub


    Private Sub FRM_EinstelSchnitt_Load()
        Try


            For Each cp In My.Computer.Ports.SerialPortNames
                C_Comport.Items.Add(cp)
            Next

            '################################################
            C_Speed.Items.Add("4800")
            'C_Speed.Items.Add("7200")

            C_Speed.Items.Add("9600")

            C_Speed.Items.Add("14400")
            C_Speed.Items.Add("19200")
            C_Speed.Items.Add("38400")

            C_Speed.Items.Add("57600")
            C_Speed.Items.Add("115200")

            '################################################

            C_Bits.Items.Add("7")
            C_Bits.Items.Add("8")

            '################################################

            C_Stoppbits.Items.Add("0")
            C_Stoppbits.Items.Add("1")
            C_Stoppbits.Items.Add("2")

            Dim parity = [Enum].GetValues(GetType(System.IO.Ports.Parity))
            Dim ptype As System.IO.Ports.Parity

            For Each ptype In parity
                C_Parity.Items.Add(ptype)
            Next ptype


            For Each Hands In [Enum].GetValues(GetType(System.IO.Ports.Handshake))
                C_HandShake.Items.Add(Hands)
            Next Hands


            C_Comport.SelectedItem = My.Settings.Port
            C_Speed.SelectedItem = My.Settings.Speed
            C_Bits.SelectedItem = My.Settings.Bits
            C_Stoppbits.SelectedItem = My.Settings.Stoppbits
            C_Parity.SelectedItem = My.Settings.Parity
            C_HandShake.SelectedItem = My.Settings.HandShake


        Catch ex As Exception
            MsgBox("na supper! hier ist der fehler --> SUB FRM_EinstelSchnitt_Load: " & vbNewLine & ex.Message.ToString)
        End Try
    End Sub

    Private Sub portsetzen()
        With MyComport1
            .PortName = C_Comport.Tag
            .BaudRate = C_Speed.Tag
            .DataBits = C_Bits.Tag
            .StopBits = C_Stoppbits.Tag
            .Parity = C_Parity.Tag
            .Handshake = C_HandShake.Tag
            .ReadTimeout = 50
            .WriteTimeout = 50
        End With
    End Sub

    Private Sub C_Comport_SelectedIndexChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles C_Comport.SelectedIndexChanged
        C_Comport.Tag = C_Comport.SelectedItem
        MyComport1.PortName = C_Comport.Tag
        My.Settings.Port = C_Comport.Tag

    End Sub

    Private Sub C_Speed_SelectedIndexChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles C_Speed.SelectedIndexChanged
        C_Speed.Tag = C_Speed.SelectedItem
        MyComport1.BaudRate = C_Speed.Tag
        My.Settings.Speed = C_Speed.Tag

    End Sub

    Private Sub C_Bits_SelectedIndexChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles C_Bits.SelectedIndexChanged
        C_Bits.Tag = C_Bits.SelectedItem
        MyComport1.DataBits = C_Bits.Tag
        My.Settings.Bits = C_Bits.Tag
    End Sub

    Private Sub C_Stoppbits_SelectedIndexChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles C_Stoppbits.SelectedIndexChanged
        C_Stoppbits.Tag = C_Stoppbits.SelectedItem
        MyComport1.StopBits = C_Stoppbits.Tag
        My.Settings.Stoppbits = C_Stoppbits.Tag
    End Sub

    Private Sub C_Parity_SelectedIndexChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles C_Parity.SelectedIndexChanged
        C_Parity.Tag = C_Parity.SelectedItem
        MyComport1.Parity = C_Parity.Tag
        My.Settings.Parity = C_Parity.Tag
    End Sub

    Private Sub C_HandShake_SelectedIndexChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles C_HandShake.SelectedIndexChanged
        C_HandShake.Tag = C_HandShake.SelectedItem
        MyComport1.Handshake = C_HandShake.Tag
        My.Settings.HandShake = C_HandShake.Tag
    End Sub

#End Region

    Private Sub initialisieren()

        Me.Icon = System.Drawing.Icon.ExtractAssociatedIcon("ViewResults.ico")

        Btn_NewNode.Image = System.Drawing.Icon.ExtractAssociatedIcon("tab.ico").ToBitmap
        ToolTip1.SetToolTip(Btn_NewNode, "Neuen Hauptast (Stamm) erstellen")

        Btn_NewSubNode.Image = Image.FromFile("note_add.png") 'System.Drawing.Icon.ExtractAssociatedIcon("tab_new.ico").ToBitmap
        ToolTip1.SetToolTip(Btn_NewSubNode, "Neuen Unter-Ast erstellen")

        BTN_DelNode.Image = Image.FromFile("note_remove.png") 'System.Drawing.Icon.ExtractAssociatedIcon("tab_remove.ico").ToBitmap
        ToolTip1.SetToolTip(BTN_DelNode, "Ast kompl. löschen")

        BTN_NewDescr.Image = Image.FromFile("note_edit.png") 'System.Drawing.Icon.ExtractAssociatedIcon("tab_remove.ico").ToBitmap
        ToolTip1.SetToolTip(BTN_NewDescr, "Beschreibung für den Ast erstellen." & vbCrLf & "Der Ast muss natürlich markiert sein." & vbCrLf & "Diese wird in AT-Befehl eingetragen!")

        Btn_Exit.Image = Image.FromFile("eject.png") 'System.Drawing.Icon.ExtractAssociatedIcon("tab_remove.ico").ToBitmap
        ToolTip1.SetToolTip(Btn_Exit, "Program verlassen")

        BTN_ClosePort.Image = Image.FromFile("phone_down.png")
        ToolTip1.SetToolTip(BTN_ClosePort, "Port schließen")

        BTN_OpenPort.Image = Image.FromFile("phone_up.png")
        ToolTip1.SetToolTip(BTN_OpenPort, "Port öffnen")

        Btn_Senden.Image = Image.FromFile("mail_next.png")
        ToolTip1.SetToolTip(Btn_Senden, "AT-Befehl senden")

        BTN_CLS.Image = Image.FromFile("page_delete.png")
        ToolTip1.SetToolTip(BTN_CLS, "Liste leeren")


        T_MSN.Text = "*"

        FRM_EinstelSchnitt_Load()

        BTN_ClosePort.Enabled = False
        BTN_OpenPort.Enabled = True
        Btn_Senden.Enabled = False

        XMLSetingsLoad()
    End Sub




#Region "XML"
   

    Sub XMLSetingsLoad()
        Try
            Dim trv As New XMLParser
            trv.importTreeViewXML(TreeView1, "XMLSettings.xml")
            TreeView1.ShowNodeToolTips = True

            For Each MyRootNodes In TreeView1.Nodes
                loadNodeState(MyRootNodes, My.Settings.NodeState)

            Next


        Catch ex As Exception
            MsgBox("na super! hier ist der Fehler --> SUB XMLSetingsload: " & vbNewLine & ex.Message.ToString)
        End Try
    End Sub

    Private Sub Btn_NewNode_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Btn_NewNode.Click
        Dim txt As String
        txt = InputBox("Überschrift eingeben", "Überschrift eingeben", "neu")
        If txt = Nothing Then Exit Sub ' Abbrechen gedrückt

        TreeView1.Nodes.Add(txt)
        SaveNewxmlSettings()

    End Sub

    Private Sub Btn_NewSubNode_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Btn_NewSubNode.Click
        Dim txt As String
        txt = InputBox("Überschrift eingeben", "Überschrift eingeben", "neu")
        If txt = Nothing Then Exit Sub ' Abbrechen gedrückt
        If (TreeView1.SelectedNode IsNot Nothing) Then
            Dim tn As TreeNode = TreeView1.SelectedNode
            tn.Nodes.Add(txt)
            SaveNewxmlSettings()
        Else
            MsgBox("nun, entweder keine Node ausgewählt oder ein Fehler ist aufgetreten!")
        End If

    End Sub

    Private Sub BTN_NewDescr_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles BTN_NewDescr.Click
        Dim txt As String

        txt = InputBox("Eintragung eingeben", "Eintragung eingeben", "neu")
        If txt = Nothing Then Exit Sub ' Abbrechen gedrückt
        If (TreeView1.SelectedNode IsNot Nothing) Then
            Dim tn As TreeNode = TreeView1.SelectedNode
            tn.Tag = (txt)
        End If
        SaveNewxmlSettings()
    End Sub

    Private Sub TreeView1_AfterSelect(ByVal sender As System.Object, ByVal e As System.Windows.Forms.TreeViewEventArgs) Handles TreeView1.AfterSelect
        If (TreeView1.SelectedNode IsNot Nothing) Then

            If (TreeView1.SelectedNode.Tag IsNot Nothing) Then
                T_ATBefehl.Text = TreeView1.SelectedNode.Tag.ToString
            Else
                T_ATBefehl.Text = ""
            End If

        End If
    End Sub

    Private Sub BTN_DelNode_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles BTN_DelNode.Click
        If MsgBox("Der Knoten wird mit Unterknoten gelöscht!" & vbCrLf & "Wirklich löschen?", vbOKCancel, "Löschen der Knoten bestätigen") = MsgBoxResult.Ok Then


            If (TreeView1.SelectedNode IsNot Nothing) Then
                Dim tn As TreeNode = TreeView1.SelectedNode
                TreeView1.Nodes.Remove(tn)
            End If
            SaveNewxmlSettings()
        End If
    End Sub

    Sub SaveNewxmlSettings()
        Dim trv As New XMLParser


        trv.exportTreeViewXML(TreeView1, "XMLSettings.xml")
    End Sub


#End Region

#Region "Treeview"

    Public Function loadNodeState(ByVal tn As TreeNode, Optional ByVal settings As String = "")
        'Jede Node in der übergebenen Node durchgenen
        'Den Zustand der Nodes wiederherstellen (Offen oder geschlossen)
        For Each tnn As TreeNode In tn.Nodes
            If tnn.Nodes.Count < 1 Then
                'Wenn der Node keine Kinder hat überspringen
            Else
                'Prüfen, ob der Node früher geöffnet war
                If settings <> "" Then
                    If settings.Substring(0, 1) = "1" Then
                        tnn.Expand()
                        tnn.EnsureVisible()
                    End If
                    settings = settings.Substring(1, settings.Length - 1)
                End If

                'Hat der node weitere "kinder" ist es ein ordner
                'also diesen node rekursiv an sich selbst übergeben!
                settings = loadNodeState(tnn, settings)
            End If
        Next
        Return settings
    End Function







    Public Function saveNodeState(ByVal tn As TreeNode, Optional ByVal retv As String = "") As String
        Dim retVal As String = retv 'retVal &
        'Jede Node in der übergebenen Node durchgenen
        For Each tnn As TreeNode In tn.Nodes
            'Prüfen, welche Nodes geöffnet sind und diesen zustand speichern
            ' 1 => offen
            ' 0 => geschlossen
            If tnn.Nodes.Count > 0 Then
                If tnn.IsExpanded Then
                    retVal += "1"
                Else
                    retVal += "0"
                End If
                'Hats der node weitere "kinder" ist es ein ordner
                'also diese node rekursiv an sich selbst übergeben!
                retVal = saveNodeState(tnn, retVal)
            End If
        Next
        Return retVal
    End Function

#End Region



  
    Private Sub TXT_Antwort_TextChanged(sender As System.Object, e As System.EventArgs) Handles TXT_Antwort.TextChanged

    End Sub
End Class
