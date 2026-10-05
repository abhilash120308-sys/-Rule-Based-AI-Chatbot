/**
 * Rule-Based AI Chatbot - Frontend Engine
 * Handles user interactions, REST API calls, real-time sanitization previews,
 * and live developer pipeline inspection.
 */

document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const chatForm = document.getElementById("chatForm");
    const userInput = document.getElementById("userInput");
    const messagesArea = document.getElementById("messagesArea");
    const welcomeCard = document.getElementById("welcomeCard");
    const previewText = document.getElementById("previewText");
    const btnClearChat = document.getElementById("btnClearChat");
    const btnExitSession = document.getElementById("btnExitSession");
    const btnRestartSession = document.getElementById("btnRestartSession");
    const sessionEndedBanner = document.getElementById("sessionEndedBanner");
    const btnSend = document.getElementById("btnSend");
    const chipsContainer = document.getElementById("chipsContainer");
    
    // Debug Panel Elements
    const btnToggleDebug = document.getElementById("btnToggleDebug");
    const btnCloseDebug = document.getElementById("btnCloseDebug");
    const debugPanel = document.getElementById("debugPanel");
    const dbgRawInput = document.getElementById("dbgRawInput");
    const dbgSanitizedInput = document.getElementById("dbgSanitizedInput");
    const dbgIntent = document.getElementById("dbgIntent");
    const dbgLookupType = document.getElementById("dbgLookupType");
    const dbgRule = document.getElementById("dbgRule");
    const dbgResponse = document.getElementById("dbgResponse");
    const dbgElapsed = document.getElementById("dbgElapsed");

    // Modal Elements
    const btnKnowledgeBase = document.getElementById("btnKnowledgeBase");
    const btnCloseModal = document.getElementById("btnCloseModal");
    const kbModal = document.getElementById("kbModal");
    const intentsTableWrapper = document.getElementById("intentsTableWrapper");

    let isSessionTerminated = false;

    // -------------------------------------------------------------
    // 1. Live Input Sanitization Preview
    // -------------------------------------------------------------
    function sanitizeClientPreview(text) {
        if (!text) return "";
        let clean = text.toLowerCase().trim();
        clean = clean.replace(/\s+/g, " ");
        clean = clean.replace(/[.?!,:;]+$/, "");
        return clean.trim();
    }

    userInput.addEventListener("input", (e) => {
        const raw = e.target.value;
        const sanitized = sanitizeClientPreview(raw);
        previewText.textContent = sanitized ? `"${sanitized}"` : "-";
    });

    // -------------------------------------------------------------
    // 2. Chat Submission Pipeline
    // -------------------------------------------------------------
    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        if (isSessionTerminated) return;

        const rawText = userInput.value;
        if (!rawText.trim()) return;

        // Hide welcome card upon first message
        if (welcomeCard) {
            welcomeCard.style.display = "none";
        }

        // Render User Message
        appendMessage("user", rawText);
        userInput.value = "";
        previewText.textContent = "-";

        // Show typing indicator
        const typingEl = showTypingIndicator();

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: rawText })
            });

            const data = await response.json();

            // Slight realistic delay before removing indicator & rendering response
            setTimeout(() => {
                removeTypingIndicator(typingEl);
                appendMessage("bot", data.response, data);
                updateDebugInspector(data);

                if (data.is_exit) {
                    handleSessionTermination();
                }
            }, 250);

        } catch (err) {
            removeTypingIndicator(typingEl);
            appendMessage("bot", "An error occurred communicating with the rule engine.", {
                matched_intent: "error",
                status: "error"
            });
            console.error("Chat API Error:", err);
        }
    });

    // -------------------------------------------------------------
    // 3. Render Message Bubbles
    // -------------------------------------------------------------
    function appendMessage(sender, text, meta = {}) {
        const row = document.createElement("div");
        row.className = `msg-row ${sender}-msg`;

        if (meta.status === "fallback") {
            row.classList.add("fallback-msg");
        } else if (meta.status === "exit" || meta.is_exit) {
            row.classList.add("exit-msg");
        }

        const avatar = document.createElement("div");
        avatar.className = "msg-avatar";
        avatar.innerHTML = sender === "user" ? "👤" : "⚡";

        const bubbleWrap = document.createElement("div");
        bubbleWrap.className = "msg-bubble-wrap";

        const bubble = document.createElement("div");
        bubble.className = "msg-bubble";
        bubble.textContent = text;

        const metaDiv = document.createElement("div");
        metaDiv.className = "msg-meta";
        const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

        if (sender === "bot" && meta.matched_intent) {
            metaDiv.innerHTML = `<span class="intent-tag">intent: ${escapeHtml(meta.matched_intent)}</span> <span>${timeStr}</span>`;
        } else {
            metaDiv.innerHTML = `<span>${timeStr}</span>`;
        }

        bubbleWrap.appendChild(bubble);
        bubbleWrap.appendChild(metaDiv);

        row.appendChild(avatar);
        row.appendChild(bubbleWrap);

        messagesArea.appendChild(row);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const row = document.createElement("div");
        row.className = "msg-row bot-msg typing-row";
        row.innerHTML = `
            <div class="msg-avatar">⚡</div>
            <div class="msg-bubble-wrap">
                <div class="msg-bubble">
                    <div class="typing-indicator">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
            </div>
        `;
        messagesArea.appendChild(row);
        scrollToBottom();
        return row;
    }

    function removeTypingIndicator(element) {
        if (element && element.parentNode) {
            element.parentNode.removeChild(element);
        }
    }

    function scrollToBottom() {
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }

    // -------------------------------------------------------------
    // 4. Update Developer Logic Inspector
    // -------------------------------------------------------------
    function updateDebugInspector(data) {
        if (!data) return;

        dbgRawInput.textContent = `"${data.raw_input || ''}"`;
        dbgSanitizedInput.textContent = `"${data.sanitized_input || ''}"`;
        dbgIntent.textContent = data.matched_intent || "unknown";
        dbgLookupType.textContent = data.lookup_type || "n/a";
        dbgRule.textContent = data.matched_rule || "Default Rule";
        dbgResponse.textContent = `"${data.response || ''}"`;
        dbgElapsed.textContent = `${data.elapsed_ms || 0.1} ms`;

        // Highlight intent color
        if (data.status === "fallback") {
            dbgIntent.className = "badge";
            dbgIntent.style.background = "rgba(245, 158, 11, 0.2)";
            dbgIntent.style.color = "#fbbf24";
        } else if (data.is_exit) {
            dbgIntent.className = "badge";
            dbgIntent.style.background = "rgba(244, 63, 94, 0.2)";
            dbgIntent.style.color = "#fda4af";
        } else {
            dbgIntent.className = "badge intent-badge";
            dbgIntent.style.background = "";
            dbgIntent.style.color = "";
        }
    }

    // -------------------------------------------------------------
    // 5. Session Termination & Restart Handlers
    // -------------------------------------------------------------
    function handleSessionTermination() {
        isSessionTerminated = true;
        userInput.disabled = true;
        btnSend.disabled = true;
        sessionEndedBanner.style.display = "block";
        userInput.placeholder = "Session closed. Click 'Restart Conversation' to begin again.";
    }

    function restartSession() {
        isSessionTerminated = false;
        userInput.disabled = false;
        btnSend.disabled = false;
        sessionEndedBanner.style.display = "none";
        userInput.placeholder = "Type a message (e.g., 'hello', 'help', 'what is your name', 'bye')...";
        userInput.focus();

        appendMessage("bot", "Session restarted. Ready for your input! Type 'help' to view options.", {
            matched_intent: "system_restart",
            status: "success"
        });
    }

    btnRestartSession.addEventListener("click", restartSession);

    btnExitSession.addEventListener("click", () => {
        if (isSessionTerminated) return;
        userInput.value = "exit";
        chatForm.dispatchEvent(new Event("submit"));
    });

    // -------------------------------------------------------------
    // 6. Clear Chat History
    // -------------------------------------------------------------
    btnClearChat.addEventListener("click", () => {
        messagesArea.innerHTML = "";
        if (welcomeCard) {
            messagesArea.appendChild(welcomeCard);
            welcomeCard.style.display = "block";
        }
        if (isSessionTerminated) {
            restartSession();
        }
    });

    // -------------------------------------------------------------
    // 7. Quick Suggestion Chips
    // -------------------------------------------------------------
    chipsContainer.addEventListener("click", (e) => {
        const chip = e.target.closest(".chip");
        if (!chip) return;

        if (isSessionTerminated) {
            restartSession();
        }

        const msg = chip.getAttribute("data-msg");
        userInput.value = msg;
        previewText.textContent = `"${sanitizeClientPreview(msg)}"`;
        chatForm.dispatchEvent(new Event("submit"));
    });

    // -------------------------------------------------------------
    // 8. Toggle Developer Inspector
    // -------------------------------------------------------------
    btnToggleDebug.addEventListener("click", () => {
        debugPanel.classList.toggle("hidden");
    });

    btnCloseDebug.addEventListener("click", () => {
        debugPanel.classList.add("hidden");
    });

    // -------------------------------------------------------------
    // 9. Knowledge Base Modal & Intents Fetching
    // -------------------------------------------------------------
    btnKnowledgeBase.addEventListener("click", async () => {
        kbModal.style.display = "flex";
        if (intentsTableWrapper.innerHTML.trim() === "") {
            try {
                intentsTableWrapper.innerHTML = `<p style="color: var(--text-dim);">Loading knowledge base...</p>`;
                const res = await fetch("/api/intents");
                const data = await res.json();

                let html = `
                    <table class="intents-table">
                        <thead>
                            <tr>
                                <th>Intent</th>
                                <th>Sample Triggers</th>
                                <th>Predefined Response</th>
                            </tr>
                        </thead>
                        <tbody>
                `;

                data.intents.forEach(item => {
                    const triggersHtml = item.sample_patterns.map(p => `<span class="pattern-chip">${escapeHtml(p)}</span>`).join(" ");
                    html += `
                        <tr>
                            <td><strong style="color: var(--cyan);">${escapeHtml(item.intent)}</strong><br><small style="color: var(--text-dim);">${escapeHtml(item.description)}</small></td>
                            <td>${triggersHtml}</td>
                            <td style="color: #cbd5e1; font-size: 0.8rem;">${escapeHtml(item.response)}</td>
                        </tr>
                    `;
                });

                html += `</tbody></table>`;
                intentsTableWrapper.innerHTML = html;
            } catch (err) {
                intentsTableWrapper.innerHTML = `<p style="color: var(--rose);">Failed to load knowledge base.</p>`;
            }
        }
    });

    btnCloseModal.addEventListener("click", () => {
        kbModal.style.display = "none";
    });

    kbModal.addEventListener("click", (e) => {
        if (e.target === kbModal) {
            kbModal.style.display = "none";
        }
    });

    // Helper: Escape HTML
    function escapeHtml(str) {
        if (!str) return "";
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // Auto-focus input on page load
    userInput.focus();
});
