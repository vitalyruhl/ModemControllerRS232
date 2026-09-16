'Author: Sebastian Gross
'Web: www.bigbasti.com
'Blog: blog.bigbasti.com
'E-mail: kontakt@bigbasti.com

'XMLParser Version 1.1

'LIZENZ: Sie können diesen Code gerne in Ihren eigenen Projekten verwenden
'sowie modifizieren und weiterentwickeln. Gerne können Sie mir auch Wünsche,
'Änderungen üder Fehler mailen.

'Ich würde mich freuen wenn Sie mir eine Kurze mail schreiben, und Ihr Projekt
'beschreiben in dem Sie diesen Code verwenden. Ich würde dann einen Back-Link
'auf meiner Homepage zu ihrem Projekt erstellen!

'Für weitere Tipps & Tricks sowie Beispiele besuchen Sie meine o.g. Homepage.

#Region "Changelog"
'Changelog:
'------------------------------------------------------------------------------
'v. 1.1 01.09.2009
'------------------------------------------------------------------------------
'* Funktionen zum exportieren & importieren von TreeViews hinzugefügt
'* Funktions-beschreibungen hinzugefügt
'* Regionen hinzugefügt
'* FIX: Die XMLNode Namen werden nun richtig gespeichert und gelesen
'* Funktionsbeschreibungen hinzugefügt
'------------------------------------------------------------------------------
'v. 1.0 21.08.2009
'------------------------------------------------------------------------------
#End Region


#Region "wie verwenden"

'' '' '' ''    Dim XMLp As New XMLParser

'' '' '' ''    'Funktionen zum Speichern/Lesen von TreeNodes seit Version 1.0:
'' '' '' ''    '--------------------------------------------------

'' '' '' ''    'Die treeview enthält einen vordefinierten Baum
'' '' '' ''    'Dieser wird zur Demonstration erst gespeichert:
'' '' '' ''    XMLp.exportTreeNodeXML(Me.trv.Nodes(0), "C:\test.xml")
'' '' '' ''    'Und dann als neuer Ast eingelesen, weswegen 2 gleiche Bäume vorhanden sind
'' '' '' ''    trv.Nodes.Add(XMLp.importTreeNodeXML("C:\test.xml"))

'' '' '' ''    'Neue Funktionen Ganze Treeview Speichern/Lesen seit version 1.1:
'' '' '' ''    '--------------------------------------------------

'' '' '' ''    'Nun wird zum Demonstrieren die gesammte TreeView (sollten 2 Bäume sein) gespeichert
'' '' '' ''    XMLp.exportTreeViewXML(trv, "C:\test2.xml")
'' '' '' ''    'nun werden alle einträge aus der TreeView entfernt
'' '' '' ''    trv.Nodes.Clear()                   'Diesen Schritt weglassen um wieder einen Verdopplungseffekt zu erzielen
'' '' '' ''    'Und die eben gespeicherte Datei wieder eingelesen
'' '' '' ''    XMLp.importTreeViewXML(trv, "C:\test2.xml")

'' '' '' ''    '=> Wenn alles gut geht sollte man 2 Gleiche Bäume sehen sollen!

'' '' '' ''    'Viel Spaß mit der Klasse!

'' '' '' ''    'Eigene Datei einlesen:
'' '' '' ''    'trv.Nodes.Add(XMLp.importTreeNodeXML("PFAD ZUR DATEI"))


'' '' '' ''        XMLp.





#End Region


Imports System.IO
Imports System.Xml

Public Class XMLParser
    'Klassenvariablen
    '---
    Dim writer As XmlWriter
    Dim retNode As TreeNode
    Dim retTree As TreeView
    Dim xmlDoc As New XmlDocument
    '---

    Public Sub New()
        'Konstruktor wird nicht benötigt
    End Sub

    ''' <summary>
    ''' Speichert eine TreeNode im XML-Format unter dem angegebenen Pfad ab.
    ''' </summary>
    ''' <param name="trn">Der TreeNode, der abgespeichert werden soll</param>
    ''' <param name="path">Der Pfad, unter dem der TreeNode abgespeichert werden soll</param>
    Public Sub exportTreeNodeXML(ByVal trn As TreeNode, ByVal path As String)
        'Prüfen, ob Zieldatei bereits exestiert, wenn ja Löschen
        If File.Exists(path) Then File.Delete(path)

        Dim settings As New XmlWriterSettings()
        settings.Indent = True
        settings.OmitXmlDeclaration = False
        'Die gewünschte Datei neu erstellen
        writer = XmlWriter.Create(path, settings)

        With writer
            .WriteStartDocument()

            .WriteStartElement(XmlConvert.EncodeName(trn.Text))

            writeNewTreeNode(trn)

            .WriteEndElement()
            .WriteEndDocument()
            .Close()
        End With

    End Sub

    ''' <summary>
    ''' Diese Funktion geht rekursiv durch alle Einträge der TreeNode
    ''' </summary>
    ''' <param name="startNode">Der TreeNode, in dem nach Weiteren Nodes gesucht werden soll</param>
    Private Sub writeNewTreeNode(ByVal startNode As TreeNode)
        For Each tn As TreeNode In startNode.Nodes
            If tn.Nodes.Count < 1 Then
                'Wenn tn ein End-Element ist, also keine Unterelemente hat
                'Neues Element erstellen
                writer.WriteStartElement(XmlConvert.EncodeName(tn.Text))


                If tn.Tag IsNot Nothing Then
                    writer.WriteAttributeString("Description", XmlConvert.EncodeName(tn.Tag.ToString))

                Else
                    writer.WriteAttributeString("Description", "")
                    'writer.WriteString(tn.Text)
                End If

                'writer.WriteString(tn.Tag.ToString) 'Innertext
                'Element schließen
                writer.WriteEndElement()
            Else
                'Wenn tn ein Node mit Unternodes ist
                'Neues Element erstellen
                writer.WriteStartElement(XmlConvert.EncodeName(tn.Text))

                writeNewTreeNode(tn)
             
                writer.WriteEndElement()
            End If


        Next
    End Sub

    ''' <summary>
    ''' Diese Funktion Liest eine XML-Datei ein und wandelt diese in ein TreeNode um
    ''' </summary>
    ''' <param name="path">Der Pfad zu der XML-Datei, die in eine TreeNode eingelesen werden soll.</param>
    Public Function importTreeNodeXML(ByVal path As String) As TreeNode
        'Try
        If File.Exists(path) Then
            xmlDoc.Load(path)
            Try
                'Lädt man ein altes Default.xml wird es einen Fehler geben
                retNode = New TreeNode(XmlConvert.DecodeName(xmlDoc.ChildNodes(1).Name))
            Catch ex As Exception
                'Wegen Abwärtskompabilität:
                retNode = New TreeNode(XmlConvert.DecodeName(xmlDoc.FirstChild.Name))
            End Try

            readNewTreeNode(retNode.Nodes, xmlDoc.DocumentElement)
        End If
        'Catch ex As Exception
        'MessageBox.Show(ex.Message, "XMLParser Error", MessageBoxButtons.OK, MessageBoxIcon.Error)
        'End Try

        Return retNode
    End Function

    ' Diese Funktion geht rekursiv durch alle Einträge der XML-Datei
    ' <param name="node">Der Treenode an den die Ausgelesenen XML-Nodes gehängt werden sollen</param>
    ' <param name="xmln">Die XML-Node aus der die Unterbereiche ausgelesen werden sollen</param>
    Private Function readNewTreeNode(ByVal node As TreeNodeCollection, ByVal xmln As XmlNode) As TreeNode
        Dim nn As TreeNode
        nn = Nothing
        For Each xn As XmlNode In xmln.ChildNodes
           If xn.Name.Equals("#text") Then
                nn = node.Add(XmlConvert.DecodeName(xn.Value))


            Else
                If xn.Attributes.Count = 0 Then
                    nn = node.Add(XmlConvert.DecodeName(xn.Name))

                Else
                    nn = node.Add(XmlConvert.DecodeName(xn.Name)) '
                    nn.ToolTipText = XmlConvert.DecodeName(xn.Attributes(0).Value)
                    nn.Tag = XmlConvert.DecodeName(xn.Attributes(0).Value)
                End If


            End If

            readNewTreeNode(nn.Nodes, xn)

        Next
        Return nn
    End Function

#Region "exportTreeView"
    ''' <summary>
    ''' Diese Funktion speichert die Angegebene TreeView im XML Format ab
    ''' </summary>
    ''' <param name="trv">Die TreeView, die als XML Datei exportiert werden soll</param>
    ''' <param name="path">Der Pfad, unter dem die XML-Datei gespeichert werden soll</param>
    Public Sub exportTreeViewXML(ByVal trv As TreeView, ByVal path As String)
        'Prüfen, ob Zieldatei bereits exestiert, wenn ja Löschen
        If File.Exists(path) Then File.Delete(path)
        Dim settings As New XmlWriterSettings()
        settings.Indent = True
        settings.CheckCharacters = False
        settings.ConformanceLevel = ConformanceLevel.Auto
        'Die gewünschte Datei neu erstellen
        writer = XmlWriter.Create(path, settings)

        'Da man in einem XML Dokument nicht mehrere Root-Elemente haben kann, 
        'eine Treeview aber mehrere enthalten kann müssen wir eine neue Node
        'um die anderen packen, die man beim einlesen wieder entfernen muss
        Dim myNode As TreeNode = New TreeNode("rootNode")
        For Each n As TreeNode In trv.Nodes
            myNode.Nodes.Add(n.Clone)
        Next

        writer.WriteStartDocument()
        With writer
            .WriteStartElement(XmlConvert.EncodeName(myNode.Text))

            writeNewTreeNode(myNode)

            .WriteEndElement()
        End With
        writer.WriteEndDocument()
        writer.Close()
    End Sub

    ''' <summary>
    ''' Diese Funktion lädt eine TreeView aus einer XML-Datei.
    ''' </summary>
    ''' <param name="trv">Die TreeView, in die die XML-Datei importiert werden soll</param>
    ''' <param name="path">Der Pfad, unter dem die XML-Datei gespeichert ist</param>
    Public Sub importTreeViewXML(ByVal trv As TreeView, ByVal path As String)
        Try
            If File.Exists(path) Then
                xmlDoc.Load(path)
                Try
                    'Lädt man ein altes Default.xml wird es einen Fehler geben
                    retNode = New TreeNode(XmlConvert.DecodeName(xmlDoc.ChildNodes(1).Name))
                Catch ex As Exception
                    'Wegen Abwärtskompabilität:
                    retNode = New TreeNode(XmlConvert.DecodeName(xmlDoc.FirstChild.Name))
                End Try

                readNewTreeNode(retNode.Nodes, xmlDoc.DocumentElement)

                For Each n As TreeNode In retNode.Nodes
                    trv.Nodes.Add(n)
                Next
            End If
        Catch ex As Exception
            MessageBox.Show(ex.Message, "XMLParser Error", MessageBoxButtons.OK, MessageBoxIcon.Error)
        End Try
    End Sub

#End Region
End Class
