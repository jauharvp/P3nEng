#!/usr/bin/env python
# -*- coding: utf-8 -*-

from burp import IBurpExtender, ITab, IMessageEditorController
from javax.swing import JPanel, JButton, JTextField, JTextArea, JLabel, JScrollPane, BoxLayout, JList, DefaultListModel
from javax.swing import BorderFactory, JSplitPane, ListSelectionModel, JOptionPane, SwingConstants, JRadioButton, ButtonGroup
from javax.swing import JTabbedPane
from java.awt import BorderLayout, Dimension, GridLayout, FlowLayout, Color
import base64
import json
import re

class BurpExtender(IBurpExtender, ITab, IMessageEditorController):

    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        self.callbacks.setExtensionName("IDOR Checker")

        # Initialize storage
        self.childToken = ""
        self.elderToken = ""
        self.originalRequests = []
        self.idorTestRequests = []
        self.parameters = []
        self.currentOriginalRequest = None
        self.currentIdorTest = None

        # Create main panel
        self.panel = JPanel(BorderLayout())

        # Top panel with controls
        topPanel = JPanel()
        topPanel.setLayout(BoxLayout(topPanel, BoxLayout.Y_AXIS))

        # JWT claim config
        claimPanel = JPanel(GridLayout(1, 2, 10, 10))
        claimPanel.setBorder(BorderFactory.createTitledBorder("JWT Claim"))
        self.claimNameField = JTextField("role", 15)
        claimPanel.add(JLabel("Role Claim:"))
        claimPanel.add(self.claimNameField)

        # JWT tokens panel
        tokenPanel = JPanel(GridLayout(2, 3, 10, 10))
        tokenPanel.setBorder(BorderFactory.createTitledBorder("JWT Tokens"))

        self.childTokenField = JTextField("", 30)
        self.elderTokenField = JTextField("", 30)

        childSaveButton = JButton("Save")
        childSaveButton.setPreferredSize(Dimension(80, 25))
        childSaveButton.addActionListener(lambda event: self.saveToken("child"))

        elderSaveButton = JButton("Save")
        elderSaveButton.setPreferredSize(Dimension(80, 25))
        elderSaveButton.addActionListener(lambda event: self.saveToken("elder"))

        tokenPanel.add(JLabel("Child Token:"))
        tokenPanel.add(self.childTokenField)
        tokenPanel.add(childSaveButton)
        tokenPanel.add(JLabel("Elder Token:"))
        tokenPanel.add(self.elderTokenField)
        tokenPanel.add(elderSaveButton)

        # Pattern input panel
        patternPanel = JPanel(BorderLayout())
        patternPanel.setBorder(BorderFactory.createTitledBorder("Add Pattern"))

        patternInputPanel = JPanel(FlowLayout(FlowLayout.LEFT))
        self.patternField = JTextField(30)

        # Radio buttons
        self.apiRadioButton = JRadioButton("API Regex", True)
        self.paramRadioButton = JRadioButton("Parameter", False)
        buttonGroup = ButtonGroup()
        buttonGroup.add(self.apiRadioButton)
        buttonGroup.add(self.paramRadioButton)

        addButton = JButton("Add")
        addButton.setPreferredSize(Dimension(80, 25))
        addButton.addActionListener(lambda event: self.addPattern())

        patternInputPanel.add(JLabel("Pattern:"))
        patternInputPanel.add(self.patternField)
        patternInputPanel.add(self.apiRadioButton)
        patternInputPanel.add(self.paramRadioButton)
        patternInputPanel.add(addButton)

        patternPanel.add(patternInputPanel, BorderLayout.CENTER)

        # Pattern lists
        listsPanel = JPanel(GridLayout(1, 2, 10, 10))

        # API regex list
        apiPanel = JPanel(BorderLayout())
        apiPanel.setBorder(BorderFactory.createTitledBorder("API Patterns"))

        self.apiListModel = DefaultListModel()
        self.apiList = JList(self.apiListModel)
        self.apiList.setSelectionMode(ListSelectionModel.SINGLE_SELECTION)
        apiScrollPane = JScrollPane(self.apiList)

        apiButtonPanel = JPanel(FlowLayout(FlowLayout.CENTER))
        removeApiButton = JButton("Remove")
        removeApiButton.addActionListener(lambda event: self.removeApiPattern())
        clearApiButton = JButton("Clear All")
        clearApiButton.addActionListener(lambda event: self.clearApiPatterns())

        apiButtonPanel.add(removeApiButton)
        apiButtonPanel.add(clearApiButton)

        apiPanel.add(apiScrollPane, BorderLayout.CENTER)
        apiPanel.add(apiButtonPanel, BorderLayout.SOUTH)

        # Add default API patterns
        self.apiListModel.addElement("/api/user/\\d+/profile")
        self.apiListModel.addElement("/api/accounts/\\d+")

        # Parameter list
        paramPanel = JPanel(BorderLayout())
        paramPanel.setBorder(BorderFactory.createTitledBorder("Parameters"))

        self.paramListModel = DefaultListModel()
        self.paramList = JList(self.paramListModel)
        self.paramList.setSelectionMode(ListSelectionModel.SINGLE_SELECTION)
        paramScrollPane = JScrollPane(self.paramList)

        paramButtonPanel = JPanel(FlowLayout(FlowLayout.CENTER))
        removeParamButton = JButton("Remove")
        removeParamButton.addActionListener(lambda event: self.removeParamPattern())
        clearParamButton = JButton("Clear All")
        clearParamButton.addActionListener(lambda event: self.clearParamPatterns())

        paramButtonPanel.add(removeParamButton)
        paramButtonPanel.add(clearParamButton)

        paramPanel.add(paramScrollPane, BorderLayout.CENTER)
        paramPanel.add(paramButtonPanel, BorderLayout.SOUTH)

        listsPanel.add(apiPanel)
        listsPanel.add(paramPanel)

        # IDOR check buttons
        buttonPanel = JPanel(FlowLayout(FlowLayout.CENTER))

        childCheckButton = JButton("IDOR Child Check")
        childCheckButton.setPreferredSize(Dimension(150, 30))
        childCheckButton.addActionListener(lambda event: self.performIdorCheck("child"))

        elderCheckButton = JButton("IDOR Elder Check")
        elderCheckButton.setPreferredSize(Dimension(150, 30))
        elderCheckButton.addActionListener(lambda event: self.performIdorCheck("elder"))

        buttonPanel.add(childCheckButton)
        buttonPanel.add(elderCheckButton)

        # Add components to top panel
        topPanel.add(claimPanel)
        topPanel.add(tokenPanel)
        topPanel.add(patternPanel)
        topPanel.add(listsPanel)
        topPanel.add(buttonPanel)

        # Results panel - using Burp's native message editors
        bottomPanel = JPanel(BorderLayout())

        # Original requests
        originalPanel = JPanel(BorderLayout())
        originalPanel.setBorder(BorderFactory.createTitledBorder("Original Requests"))

        self.originalListModel = DefaultListModel()
        self.originalList = JList(self.originalListModel)
        self.originalList.setSelectionMode(ListSelectionModel.SINGLE_SELECTION)
        self.originalList.addListSelectionListener(lambda event: self.showOriginalDetails())
        originalScrollPane = JScrollPane(self.originalList)

        # Use Burp's native message editors for request/response
        self.originalRequestViewer = callbacks.createMessageEditor(self, False)
        self.originalResponseViewer = callbacks.createMessageEditor(self, False)

        # Create a tabbed pane for request/response
        originalTabbedPane = JTabbedPane()
        originalTabbedPane.addTab("Request", self.originalRequestViewer.getComponent())
        originalTabbedPane.addTab("Response", self.originalResponseViewer.getComponent())

        originalSplitPane = JSplitPane(JSplitPane.VERTICAL_SPLIT, originalScrollPane, originalTabbedPane)
        originalSplitPane.setResizeWeight(0.3)
        originalPanel.add(originalSplitPane, BorderLayout.CENTER)

        # IDOR test requests
        idorPanel = JPanel(BorderLayout())
        idorPanel.setBorder(BorderFactory.createTitledBorder("IDOR Test Requests"))

        self.idorListModel = DefaultListModel()
        self.idorList = JList(self.idorListModel)
        self.idorList.setSelectionMode(ListSelectionModel.SINGLE_SELECTION)
        self.idorList.addListSelectionListener(lambda event: self.showIdorDetails())
        idorScrollPane = JScrollPane(self.idorList)

        # Use Burp's native message editors for test request/response
        self.idorRequestViewer = callbacks.createMessageEditor(self, False)
        self.idorResponseViewer = callbacks.createMessageEditor(self, False)

        # Create a tabbed pane for test request/response
        idorTabbedPane = JTabbedPane()
        idorTabbedPane.addTab("Request", self.idorRequestViewer.getComponent())
        idorTabbedPane.addTab("Response", self.idorResponseViewer.getComponent())

        idorSplitPane = JSplitPane(JSplitPane.VERTICAL_SPLIT, idorScrollPane, idorTabbedPane)
        idorSplitPane.setResizeWeight(0.3)
        idorPanel.add(idorSplitPane, BorderLayout.CENTER)

        # Analysis panel
        analysisPanel = JPanel(BorderLayout())
        analysisPanel.setLayout(BoxLayout(analysisPanel, BoxLayout.Y_AXIS))

        # Token analysis
        tokenPanel = JPanel(BorderLayout())
        tokenPanel.setBorder(BorderFactory.createTitledBorder("JWT Analysis"))
        self.tokenAnalysisArea = JTextArea()
        self.tokenAnalysisArea.setEditable(False)
        self.tokenAnalysisArea.setLineWrap(True)
        self.tokenAnalysisArea.setWrapStyleWord(True)
        tokenScrollPane = JScrollPane(self.tokenAnalysisArea)
        tokenPanel.add(tokenScrollPane, BorderLayout.CENTER)

        # Vulnerability status
        vulnPanel = JPanel(BorderLayout())
        vulnPanel.setBorder(BorderFactory.createTitledBorder("Vulnerability Status"))
        self.vulnArea = JTextArea()
        self.vulnArea.setEditable(False)
        self.vulnArea.setLineWrap(True)
        self.vulnArea.setWrapStyleWord(True)
        vulnScrollPane = JScrollPane(self.vulnArea)
        vulnPanel.add(vulnScrollPane, BorderLayout.CENTER)

        analysisPanel.add(tokenPanel)
        analysisPanel.add(vulnPanel)

        # Organize panels
        requestsSplitPane = JSplitPane(JSplitPane.HORIZONTAL_SPLIT, originalPanel, idorPanel)
        requestsSplitPane.setResizeWeight(0.5)

        mainSplitPane = JSplitPane(JSplitPane.HORIZONTAL_SPLIT, requestsSplitPane, analysisPanel)
        mainSplitPane.setResizeWeight(0.7)

        bottomPanel.add(mainSplitPane, BorderLayout.CENTER)

        # Add panels to main frame
        overallSplitPane = JSplitPane(JSplitPane.VERTICAL_SPLIT, topPanel, bottomPanel)
        overallSplitPane.setResizeWeight(0.3)

        self.panel.add(overallSplitPane, BorderLayout.CENTER)

        # Register tab
        callbacks.addSuiteTab(self)

        print("IDOR Checker loaded")

    # Required methods for IMessageEditorController interface
    def getHttpService(self):
        if self.currentOriginalRequest:
            return self.currentOriginalRequest.getHttpService()
        return None

    def getRequest(self):
        if self.currentOriginalRequest:
            return self.currentOriginalRequest.getRequest()
        return None

    def getResponse(self):
        if self.currentOriginalRequest:
            return self.currentOriginalRequest.getResponse()
        return None

    def getTabCaption(self):
        return "IDOR Checker"

    def getUiComponent(self):
        return self.panel

    def saveToken(self, tokenType):
        token = ""
        if tokenType == "child":
            token = self.childToken = self.childTokenField.getText()
        else:
            token = self.elderToken = self.elderTokenField.getText()

        # Analyze token
        tokenInfo = "Token saved successfully"

        try:
            claimName = self.claimNameField.getText().strip()
            claims, claimValue = self.analyzeJWT(token, claimName)

            tokenInfo += "\n\nToken Claims:\n" + claims

            if claimValue:
                tokenInfo += "\n\nRole Claim '" + claimName + "' value: " + claimValue
            else:
                tokenInfo += "\n\nRole Claim '" + claimName + "' not found in token"

        except:
            tokenInfo += "\n\nUnable to parse token as JWT."

        JOptionPane.showMessageDialog(None, tokenInfo, "Token Saved", JOptionPane.INFORMATION_MESSAGE)

    def analyzeJWT(self, token, claimName=None):
        parts = token.split('.')
        if len(parts) != 3:
            return "Invalid JWT format", None

        try:
            # Decode the payload (second part)
            payload = parts[1]
            # Add padding if needed
            payload += '=' * (4 - len(payload) % 4) if len(payload) % 4 else ''
            # Replace URL-safe characters
            payload = payload.replace('-', '+').replace('_', '/')

            decoded = base64.b64decode(payload)
            claims = json.loads(decoded)

            # Format claims for display
            result = ""
            for key, value in claims.items():
                result += "%s: %s\n" % (key, value)

            # Get specific claim if requested
            specificClaimValue = None
            if claimName and claimName in claims:
                specificClaimValue = str(claims[claimName])

            return result, specificClaimValue
        except Exception as e:
            return "Error parsing JWT: %s" % str(e), None

    def addPattern(self):
        pattern = self.patternField.getText().strip()

        if not pattern:
            JOptionPane.showMessageDialog(None, "Please enter a pattern", "Error", JOptionPane.ERROR_MESSAGE)
            return

        if self.apiRadioButton.isSelected():
            # Add to API regex list
            self.apiListModel.addElement(pattern)
        else:
            # Add to parameter list
            if "=" in pattern:
                name, value = pattern.split("=", 1)
                self.parameters.append({
                    "name": name.strip(),
                    "value": value.strip()
                })
            else:
                self.parameters.append({
                    "name": pattern,
                    "value": ""
                })

            self.paramListModel.addElement(pattern)

        self.patternField.setText("")

    def removeApiPattern(self):
        selectedIndex = self.apiList.getSelectedIndex()
        if selectedIndex != -1:
            self.apiListModel.remove(selectedIndex)
        else:
            JOptionPane.showMessageDialog(None, "Please select a pattern to remove", "Error", JOptionPane.ERROR_MESSAGE)

    def clearApiPatterns(self):
        self.apiListModel.clear()

    def removeParamPattern(self):
        selectedIndex = self.paramList.getSelectedIndex()
        if selectedIndex != -1 and selectedIndex < len(self.parameters):
            del self.parameters[selectedIndex]
            self.paramListModel.remove(selectedIndex)
        else:
            JOptionPane.showMessageDialog(None, "Please select a parameter to remove", "Error", JOptionPane.ERROR_MESSAGE)

    def clearParamPatterns(self):
        self.parameters = []
        self.paramListModel.clear()

    def showOriginalDetails(self):
        selectedIndex = self.originalList.getSelectedIndex()
        if selectedIndex != -1 and selectedIndex < len(self.originalRequests):
            # Update current request for message editors
            self.currentOriginalRequest = self.originalRequests[selectedIndex]

            # Set message in Burp's native message editors
            self.originalRequestViewer.setMessage(self.currentOriginalRequest.getRequest(), True)
            self.originalResponseViewer.setMessage(self.currentOriginalRequest.getResponse(), False)

            # Show token analysis for the corresponding IDOR test
            if selectedIndex < len(self.idorTestRequests):
                self.tokenAnalysisArea.setText(self.idorTestRequests[selectedIndex]["tokenAnalysis"])

                # Set IDOR test in the editors
                self.idorRequestViewer.setMessage(self.idorTestRequests[selectedIndex]["requestBytes"], True)
                self.idorResponseViewer.setMessage(self.idorTestRequests[selectedIndex]["responseBytes"], False)

                # Select the corresponding IDOR test in the list
                self.idorList.setSelectedIndex(selectedIndex)
            else:
                self.tokenAnalysisArea.setText("")

    def showIdorDetails(self):
        selectedIndex = self.idorList.getSelectedIndex()
        if selectedIndex != -1 and selectedIndex < len(self.idorTestRequests):
            requestInfo = self.idorTestRequests[selectedIndex]

            # Set message in Burp's native message editors
            self.idorRequestViewer.setMessage(requestInfo["requestBytes"], True)
            self.idorResponseViewer.setMessage(requestInfo["responseBytes"], False)

            # Show token analysis
            self.tokenAnalysisArea.setText(requestInfo["tokenAnalysis"])

            # Select the corresponding original request in the list
            self.originalList.setSelectedIndex(selectedIndex)

    def performIdorCheck(self, targetRole):
        # Clear previous results
        self.originalListModel.clear()
        self.idorListModel.clear()
        self.vulnArea.setText("")
        self.tokenAnalysisArea.setText("")
        self.originalRequests = []
        self.idorTestRequests = []

        # Reset message editors
        self.originalRequestViewer.setMessage(None, False)
        self.originalResponseViewer.setMessage(None, False)
        self.idorRequestViewer.setMessage(None, False)
        self.idorResponseViewer.setMessage(None, False)

        # Check if tokens are set
        if not self.childToken or not self.elderToken:
            JOptionPane.showMessageDialog(None, "Please save both tokens before testing",
                                       "Missing Tokens", JOptionPane.WARNING_MESSAGE)
            return

        # Get active proxy history
        proxyHistory = self.callbacks.getProxyHistory()

        if not proxyHistory or len(proxyHistory) == 0:
            JOptionPane.showMessageDialog(None, "No proxy history available",
                                       "Empty History", JOptionPane.WARNING_MESSAGE)
            return

        # Get regex patterns
        apiPatterns = []
        for i in range(self.apiListModel.getSize()):
            apiPatterns.append(self.apiListModel.getElementAt(i))

        if not apiPatterns and not self.parameters:
            JOptionPane.showMessageDialog(None, "Please add at least one pattern",
                                       "No Patterns", JOptionPane.WARNING_MESSAGE)
            return

        # Find matching requests
        matchingRequests = []
        matchReasons = []

        for historyItem in proxyHistory:
            requestInfo = self.helpers.analyzeRequest(historyItem)
            url = requestInfo.getUrl().toString()

            # Check API patterns
            apiMatch = False
            matchingPattern = ""

            for pattern in apiPatterns:
                try:
                    if re.search(pattern, url):
                        apiMatch = True
                        matchingPattern = pattern
                        break
                except:
                    continue

            # Check parameters
            paramMatch = self.checkParamMatch(historyItem)

            # Include if either matches
            if apiMatch or paramMatch:
                matchingRequests.append(historyItem)

                reasons = []
                if apiMatch:
                    reasons.append("API: " + matchingPattern)
                if paramMatch:
                    reasons.append("Parameter match")

                matchReasons.append(", ".join(reasons))

        if not matchingRequests:
            JOptionPane.showMessageDialog(None, "No matching requests found",
                                       "No Matches", JOptionPane.INFORMATION_MESSAGE)
            return

        # Process matching requests
        claimName = self.claimNameField.getText().strip()
        testToken = self.childToken if targetRole == "child" else self.elderToken

        # Count of vulnerabilities found
        vulnerableCount = 0

        for i, request in enumerate(matchingRequests):
            requestInfo = self.helpers.analyzeRequest(request)
            url = requestInfo.getUrl().toString()

            # Store original request
            self.originalRequests.append(request)
            self.originalListModel.addElement("%d. %s %s (%s)" % (i+1, requestInfo.getMethod(), url, matchReasons[i]))

            reqText = self.helpers.bytesToString(request.getRequest())
            respText = self.helpers.bytesToString(request.getResponse())

            # Extract and analyze tokens
            origToken = self.extractAuthToken(reqText)
            tokenAnalysis = ""

            if origToken:
                claims, claimValue = self.analyzeJWT(origToken, claimName)
                tokenAnalysis = "Original Token:\n" + claims + "\n\n"

                if claimValue:
                    tokenAnalysis += "Role: %s\n\n" % claimValue

                testClaims, testClaimValue = self.analyzeJWT(testToken, claimName)
                tokenAnalysis += "Test Token (%s):\n" % targetRole + testClaims

                if testClaimValue:
                    tokenAnalysis += "\nRole: %s" % testClaimValue
            else:
                tokenAnalysis = "No original token found\n\nTest Token (%s):\n" % targetRole
                testClaims, testClaimValue = self.analyzeJWT(testToken, claimName)
                tokenAnalysis += testClaims

            # Create modified request with test token
            headers = requestInfo.getHeaders()
            modifiedHeaders = []
            tokenFound = False

            for header in headers:
                if header.lower().startswith("authorization:"):
                    modifiedHeaders.append("Authorization: Bearer " + testToken)
                    tokenFound = True
                else:
                    modifiedHeaders.append(header)

            # Ensure we have an Authorization header
            if not tokenFound:
                modifiedHeaders.append("Authorization: Bearer " + testToken)

            # Build request
            reqBody = ""
            if "\r\n\r\n" in reqText:
                reqBody = reqText.split("\r\n\r\n", 1)[1]

            modifiedRequest = self.helpers.buildHttpMessage(modifiedHeaders, reqBody)

            # Send request
            httpService = request.getHttpService()
            modifiedResponse = self.callbacks.makeHttpRequest(
                httpService.getHost(),
                httpService.getPort(),
                httpService.getProtocol() == "https",
                modifiedRequest
            )

            modifiedResponseText = self.helpers.bytesToString(modifiedResponse)

            # Check for vulnerability
            origStatusCode = self.getStatusCode(respText)
            modStatusCode = self.getStatusCode(modifiedResponseText)

            isVulnerable = False
            reason = ""

            if origStatusCode == 200 and modStatusCode == 200:
                isVulnerable = True
                reason = "Both requests returned 200 OK (Potential IDOR)"
                vulnerableCount += 1
            elif origStatusCode == 200 and (modStatusCode == 401 or modStatusCode == 403):
                isVulnerable = False
                reason = "Proper auth checks in place (returns %d)" % modStatusCode
            else:
                if origStatusCode == modStatusCode:
                    isVulnerable = True
                    reason = "Same status code (%d) with different token" % origStatusCode
                    vulnerableCount += 1
                else:
                    isVulnerable = False
                    reason = "Different status codes: Original %d, Modified %d" % (origStatusCode, modStatusCode)

            # Store test info
            testInfo = {
                "request": self.helpers.bytesToString(modifiedRequest),
                "response": modifiedResponseText,
                "requestBytes": modifiedRequest,
                "responseBytes": modifiedResponse,
                "isVulnerable": isVulnerable,
                "reason": reason,
                "tokenAnalysis": tokenAnalysis
            }

            self.idorTestRequests.append(testInfo)
            label = "[VULN] " if isVulnerable else "[SAFE] "
            self.idorListModel.addElement("%d. %s%s %s (%s token)" %
                                       (i+1, label, requestInfo.getMethod(), url, targetRole))

            # Update vulnerability area
            status = "[VULNERABLE]" if isVulnerable else "[NOT VULNERABLE]"
            self.vulnArea.append("%s %s\n" % (status, url))
            self.vulnArea.append("Original: %d, Modified: %d\n" % (origStatusCode, modStatusCode))
            self.vulnArea.append("Reason: %s\n\n" % reason)

        # Summary
        self.vulnArea.append("\n--- IDOR Test Summary ---\n")
        self.vulnArea.append("Total requests tested: %d\n" % len(matchingRequests))
        self.vulnArea.append("Potential vulnerabilities found: %d\n" % vulnerableCount)

        # Select first item
        if self.originalListModel.getSize() > 0:
            self.originalList.setSelectedIndex(0)

    def checkParamMatch(self, request):
        if not self.parameters:
            return False

        requestInfo = self.helpers.analyzeRequest(request)

        # Get parameters
        requestParams = requestInfo.getParameters()

        # Check each parameter
        for param in self.parameters:
            paramName = param["name"]
            paramValue = param["value"]

            for reqParam in requestParams:
                if reqParam.getName() == paramName:
                    if not paramValue or str(reqParam.getValue()) == paramValue:
                        return True

        return False

    def extractAuthToken(self, requestText):
        lines = requestText.split('\n')
        for line in lines:
            if line.lower().startswith("authorization:"):
                parts = line.split()
                if len(parts) >= 3 and parts[1].lower() == "bearer":
                    return parts[2]
        return None

    def getStatusCode(self, responseText):
        if responseText:
            statusLine = responseText.split("\n")[0]
            parts = statusLine.split(" ")
            if len(parts) >= 2:
                try:
                    return int(parts[1])
                except:
                    return 0
        return 0
