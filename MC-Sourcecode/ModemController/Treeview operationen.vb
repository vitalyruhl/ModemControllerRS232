'Public Class Form1

'    Private Sub TreeViewSpeichernToolStripMenuItem_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TreeViewSpeichernToolStripMenuItem.Click
'        Dim fs As SaveFileDialog = New SaveFileDialog
'        fs.ShowDialog()

'        IO.File.WriteAllText(fs.FileName, saveNodeState(TreeView1.Nodes(0)))
'    End Sub

'    Public Function loadNodeState(ByVal tn As TreeNode, Optional ByVal settings As String = "")
'        'Jede Node in der übergebenen Node durchgenen
'        'Den Zustand der Nodes wiederherstellen (Offen oder geschlossen)
'        For Each tnn As TreeNode In tn.Nodes
'            If tnn.Nodes.Count < 1 Then
'                'Wenn der Node keine Kinder hat überspringen
'            Else
'                'Prüfen, ob der Node früher geöffnet war
'                If settings <> "" Then
'                    If settings.Substring(0, 1) = "1" Then
'                        tnn.Expand()
'                    End If
'                    settings = settings.Substring(1, settings.Length - 1)
'                End If

'                'Hat der node weitere "kinder" ist es ein ordner
'                'also diesen node rekursiv an sich selbst übergeben!
'                settings = loadNodeState(tnn, settings)
'            End If
'        Next
'        Return settings
'    End Function

'    Public Function saveNodeState(ByVal tn As TreeNode, Optional ByVal retv As String = "") As String
'        Dim retVal As String = retVal & retv
'        'Jede Node in der übergebenen Node durchgenen
'        For Each tnn As TreeNode In tn.Nodes
'            'Prüfen, welche Nodes geöffnet sind und diesen zustand speichern
'            ' 1 => offen
'            ' 0 => geschlossen
'            If tnn.Nodes.Count > 0 Then
'                If tnn.IsExpanded Then
'                    retVal = retVal & "1"
'                Else
'                    retVal = retVal & "0"
'                End If
'                'Hats der node weitere "kinder" ist es ein ordner
'                'also diese node rekursiv an sich selbst übergeben!
'                retVal = saveNodeState(tnn, retVal)
'            End If
'        Next
'        Return retVal
'    End Function

'    Private Sub TreeViewStatusLadenToolStripMenuItem_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TreeViewStatusLadenToolStripMenuItem.Click
'        Dim fs As OpenFileDialog = New OpenFileDialog
'        fs.ShowDialog()

'        loadNodeState(TreeView1.Nodes(0), IO.File.ReadAllText(fs.FileName))
'        TreeView1.Nodes(0).Expand()
'    End Sub
'End Class
