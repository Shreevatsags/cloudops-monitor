import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function CreateApplication() {
  const [name, setName] = useState("");
  const [repositoryUrl, setRepositoryUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!name.trim() || !repositoryUrl.trim()) {
      alert("Please fill in all fields");
      return;
    }

    setLoading(true);

    try {
      const response = await api.post("/applications/", {
        name: name.trim(),
        repository_url: repositoryUrl.trim(),
      });

      console.log("Application created:", response.data);

      alert("Application created successfully!");

      navigate("/applications");
    } catch (error) {
      console.error("Create application error:", error);

      if (error.response) {
        console.error("Status:", error.response.status);
        console.error("Response:", error.response.data);

        alert(
          error.response.data?.detail ||
            `Failed to create application (${error.response.status})`
        );
      } else if (error.request) {
        console.error("No response received:", error.request);

        alert(
          "Backend is not responding. Make sure the backend is running."
        );
      } else {
        console.error("Request error:", error.message);

        alert(`Failed to create application: ${error.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl">
      <h1 className="text-3xl font-bold mb-8">
        Create Application
      </h1>

      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-xl shadow-sm space-y-6"
      >
        <div>
          <label className="block font-medium mb-2">
            Application Name
          </label>

          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Healthcare API"
            className="w-full border rounded-lg px-4 py-3"
            required
          />
        </div>

        <div>
          <label className="block font-medium mb-2">
            GitHub Repository
          </label>

          <input
            type="url"
            value={repositoryUrl}
            onChange={(e) =>
              setRepositoryUrl(e.target.value)
            }
            placeholder="https://github.com/user/project"
            className="w-full border rounded-lg px-4 py-3"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="bg-slate-900 text-white px-5 py-3 rounded-lg disabled:opacity-50"
        >
          {loading
            ? "Creating..."
            : "Create Application"}
        </button>
      </form>
    </div>
  );
}

export default CreateApplication;