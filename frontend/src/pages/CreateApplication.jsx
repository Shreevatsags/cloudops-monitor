import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function CreateApplication() {

  const [name, setName] = useState("");
  const [repositoryUrl, setRepositoryUrl] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (e) => {

    e.preventDefault();

    try {

      await api.post("/applications/", {
        name,
        repository_url: repositoryUrl,
      });

      navigate("/applications");

    } catch (error) {

      console.error(error);

      alert("Failed to create application");

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
            onChange={(e) =>
              setName(e.target.value)
            }
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
          className="bg-slate-900 text-white px-5 py-3 rounded-lg"
        >
          Create Application
        </button>

      </form>

    </div>

  );
}

export default CreateApplication;