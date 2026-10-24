const API_BASE_URL = "http://127.0.0.1:8000";

export async function cloneRepository(repoUrl) {
  try {
    const response = await fetch(`${API_BASE_URL}/repo/clone`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ repo_url: repoUrl }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to clone repository.");
    }

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}