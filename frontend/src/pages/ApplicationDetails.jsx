import { useEffect, useState } from "react";
import {
  useNavigate,
  useParams
} from "react-router-dom";

import api from "../services/api";


function ApplicationDetails() {

  const { id } = useParams();

  const navigate = useNavigate();

  const [application, setApplication] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [deploying, setDeploying] =
    useState(false);


  // Fetch application details
  useEffect(() => {

    const fetchApplication = async () => {

      try {

        const response = await api.get(
          `/applications/${id}`
        );

        setApplication(response.data);

      } catch (error) {

        console.error(
          "Failed to fetch application:",
          error
        );

      } finally {

        setLoading(false);

      }

    };

    fetchApplication();

  }, [id]);

  // Build application
 const handleBuild = async () => {

  try {

    await api.post(
      `/applications/${id}/build`
    );

    alert("Docker image built successfully!");

    window.location.reload();

  } catch (error) {

    console.error(
      "Build failed:",
      error
    );

    alert(
      error.response?.data?.detail ||
      "Build failed"
    );
  }
};

  // Deploy application
  const handleDeploy = async () => {

  setDeploying(true);

  try {

    await api.post(
      `/deployments/${id}`
    );

    alert("Deployment created successfully!");

    navigate("/deployments");

  } catch (error) {

    console.error(
      "Deployment failed:",
      error
    );

    alert("Deployment failed.");

  } finally {

    setDeploying(false);

  }
};


  // Loading state
  if (loading) {

    return (
      <div className="p-8">
        <p className="text-slate-500">
          Loading application...
        </p>
      </div>
    );

  }


  // Application not found
  if (!application) {

    return (
      <div className="p-8">

        <h1 className="text-2xl font-bold">
          Application not found
        </h1>

        <button
          onClick={() => navigate("/applications")}
          className="mt-4 bg-slate-900 text-white px-5 py-3 rounded-lg"
        >
          Back to Applications
        </button>

      </div>
    );

  }


  return (

    <div>

      {/* Header */}

      <div className="flex justify-between items-center mb-8">

        <div>

          <h1 className="text-3xl font-bold text-slate-900">
            {application.name}
          </h1>

          <p className="text-slate-500 mt-2">
            Application details and deployment information
          </p>

        </div>


        <button
          onClick={() => navigate("/applications")}
          className="border border-slate-300 px-4 py-2 rounded-lg hover:bg-slate-100"
        >
          Back
        </button>

      </div>


      {/* Application Information */}

      <div className="bg-white p-6 rounded-xl shadow-sm">

        <h2 className="text-xl font-semibold mb-6">
          Application Information
        </h2>


        {/* Status */}

        <div className="mb-5">

          <p className="text-sm text-slate-500">
            Status
          </p>

          <p className="mt-1 font-medium text-green-600">
            {application.status}
          </p>

        </div>


        {/* Repository */}

        <div className="mb-5">

          <p className="text-sm text-slate-500">
            Repository
          </p>

          <a
            href={application.repository_url}
            target="_blank"
            rel="noreferrer"
            className="mt-1 block text-blue-600 hover:underline"
          >
            {application.repository_url}
          </a>

        </div>


        {/* Docker Image */}

        <div className="mb-5">

          <p className="text-sm text-slate-500">
            Docker Image
          </p>

          <p className="mt-1">
            {application.docker_image ||
              "Not built yet"}
          </p>
        

        </div>


        {/* Deploy Button */}

        <div className="border-t pt-6">

          {application.status !== "built" ? (

    <button
      onClick={handleBuild}
      className="bg-slate-900 text-white px-6 py-3 rounded-lg hover:bg-slate-800"
   >
      Build Application
    </button>

  ) : (

    <button
      onClick={handleDeploy}
      disabled={deploying}
      className="bg-slate-900 text-white px-6 py-3 rounded-lg hover:bg-slate-800 disabled:opacity-50"
    >
      {deploying
        ? "Creating Deployment..."
        : "Deploy Application"}
    </button>

    )}

        </div>

      </div>

    </div>

  );
}


export default ApplicationDetails;