// Helper functions for n8n workflow
function preprocessQuestion(question) {
    if (!question || question.trim().length === 0) {
        throw new Error("Question cannot be empty");
    }
    return question.trim().toLowerCase();
}

function routeQuestion(question) {
    const greetings = ["hello", "hi", "hey"];
    const capabilities = ["what can you", "how do you", "abilities"];
    
    if (greetings.some(g => question.includes(g))) {
        return { agent: "greeting" };
    }
    
    if (capabilities.some(c => question.includes(c))) {
        return { agent: "capabilities" };
    }
    
    return { agent: "rag" };
}

module.exports = {
    preprocessQuestion,
    routeQuestion
};