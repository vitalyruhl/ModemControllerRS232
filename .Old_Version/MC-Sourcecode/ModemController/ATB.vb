Imports System.IO
Public Class F_Settings

    Private Sub BTN_Cancel_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles BTN_Cancel.Click
        Me.Close()
    End Sub

    Private Sub BTN_Save_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles BTN_Save.Click

        SaveFileDialog1.DefaultExt = "VCE"
        SaveFileDialog1.AddExtension = True
        SaveFileDialog1.InitialDirectory = My.Computer.FileSystem.CurrentDirectory.ToString
        SaveFileDialog1.ShowDialog()
        If SaveFileDialog1.CheckFileExists = True Then
            'Überschreiben?
            If MsgBox("Datei existiert bereits! Überschreiben?", MsgBoxStyle.YesNo) = MsgBoxResult.Yes Then
                SaveMyFile(SaveFileDialog1.FileName)

            Else
                SaveFileDialog1.ShowDialog()
            End If
        ElseIf SaveFileDialog1.FileName = Nothing Then
            MsgBox("Keine Datei ausgewählt")
        Else
            SaveMyFile(SaveFileDialog1.FileName)
        End If
    End Sub

    Sub SaveMyFile(ByVal MyFileName As String)

        Dim sw As New StreamWriter(MyFileName, False)
        Dim ctrl As Control

        Try



            For Each ctrl In Me.Controls

                If TypeOf ctrl Is TextBox Then

                    sw.WriteLine(ctrl.Text.ToUpper)
                End If

            Next
            sw.WriteLine("")
            sw.Flush()
            sw.Close()
            Me.Close()
        Catch ex As Exception
            MsgBox("na ja hier ist der fehler --> " & vbNewLine & ex.Message.ToString)
            sw.Flush()
            sw.Close()
            Me.Close()
        End Try
    End Sub


    Private Sub F_Settings_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        Dim loadoN As String = GetSetting("Modem Controller", "TempVar", "Dat")

        If loadoN = "Neu" Then
            L_Datei.Text = loadoN

        Else
            'daten laden
            loadDaten(loadoN)
            L_Datei.Text = loadoN
        End If

    End Sub

    Private Sub loadDaten(ByVal Datei As String)
        Dim sw As New StreamReader(My.Computer.FileSystem.CurrentDirectory.ToString & "\" & Datei)
        Dim temp As String

        Try
            For Each ctrl In Me.Controls

                If TypeOf ctrl Is TextBox Then

                    temp = sw.ReadLine.ToString

                    If temp = Nothing Then
                        Exit For
                    Else
                        ctrl.Text = temp
                    End If

                End If

            Next

        Catch ex As Exception
            MsgBox("na supper! hier ist der fehler --> SUB Lade Daten: " & vbNewLine & ex.Message.ToString)
        Finally
            sw.Close()
        End Try



    End Sub
End Class