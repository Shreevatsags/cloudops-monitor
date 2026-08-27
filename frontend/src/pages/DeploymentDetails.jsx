import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../services/api";

function DeploymentDetails() {

  const { id } = useParams();

  const [deployment, setDeployment] = useState(null);
  const [logs, setLogs] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionLoading, setActionLoading] = useState(false);

  const handleStop = async () => {

  setActionLoading(true);

  try {

    const response = await api.post(
      `/deployments/${id}/stop`
    );

    setDeployment((prev) => ({
      ...prev,
      status: response.data.status
    }));

    alert("Deployment stopped successfully.");

  } catch (error) {

    console.error(
      "Failed to stop deployment:",
      error
    );

    alert(
      error.response?.data?.detail ||
      "Failed to stop deployment."
    );

  } finally {

    setActionLoading(false);

  }
};


    const handleRestart = async () => {

      setActionLoading(true);

    try {

    const response = await api.post(
      `/deployments/${id}/restart`
    );

    setDeployment((prev) => ({
      ...prev,
      status: response.data.status
    }));

    alert("Deployment restarted successfully.");

  } catch (error) {

    console.error(
      "Failed to restart deployment:",
      error
    );

    alert(
      error.response?.data?.detail ||
      "Failed to restart deployment."
    );

  } finally {

    setActionLoading(false);

  }
};

  useEffect(() => {

    const fetchDeployment = async () => {

      try {

        // Get all deployments
        const deploymentResponse =
          await api.get("/deployments/");

        const currentDeployment =
          deploymentResponse.data.find(
            (item) =>
              item.id === Number(id)
          );

        if (!currentDeployment) {
          setError("Deployment not found.");
          return;
        }

        setDeployment(currentDeployment);


        // Get deployment logs
        const logsResponse =
          await api.get(
            `/deployments/${id}/logs`
          );

        setLogs(logsResponse.data);

      } catch (error) {

        console.error(
          "Failed to fetch deployment:",
          error
        );

        setError(
          error.response?.data?.detail ||
          "Failed to load deployment."
        );

      } finally {

        setLoading(false);

      }

    };

    fetchDeployment();

  }, [id]);


  if (loading) {

    return (
      <div className="p-8">
        <p className="text-slate-500">
          Loading deployment...
        </p>
      </div>
    );

  }


  if (error) {

    return (
      <div className="p-8">

        <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg">
          {error}
        </div>

        <Link
          to="/deployments"
          className="inline-block mt-5 text-blue-600 hover:underline"
        >
          ← Back to Deployments
        </Link>

      </div>
    );

  }


  return (

    <div>

      {/* Header */}

      <div className="flex justify-between items-center mb-8">

        <div>

          <h1 className="text-3xl font-bold text-slate-900">
            Deployment #{deployment.id}
          </h1>

          <p className="text-slate-500 mt-2">
            Deployment information and logs
          </p>

        </div>

        <Link
          to="/deployments"
          className="border border-slate-300 px-4 py-2 rounded-lg hover:bg-slate-100"
        >
          Back
        </Link>

      </div>


      {/* Deployment Information */}

      <div className="bg-white rounded-xl shadow-sm p-6 mb-8">

        <h2 className="text-xl font-semibold mb-6">
          Deployment Information
        </h2>


        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">


          {/* Application */}

          <div>

            <p className="text-sm text-slate-500">
              Application ID
            </p>

            <p className="mt-1 font-medium">
              {deployment.application_id}
            </p>

          </div>


          {/* Version */}

          <div>

            <p className="text-sm text-slate-500">
              Version
            </p>

            <p className="mt-1 font-medium">
              {deployment.version}
            </p>

          </div>


          {/* Status */}

          <div>

            <p className="text-sm text-slate-500">
              Status
            </p>

            <span
              className={
                deployment.status === "success"
                  ? "inline-block mt-1 px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-700"
                  : deployment.status === "failed"
                  ? "inline-block mt-1 px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-700"
                  : "inline-block mt-1 px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-700"
              }
            >
              {deployment.status}
            </span>

          </div>
          <div className="flex gap-3 mt-6">

  <button
    onClick={handleStop}
    disabled={
      actionLoading ||
      deployment.status === "stopped"
    }
    className="bg-red-600 text-white px-5 py-3 rounded-lg hover:bg-red-700 disabled:opacity-50"
  >
    {actionLoading
      ? "Processing..."
      : "Stop Deployment"}
  </button>


  <button
    onClick={handleRestart}
    disabled={
      actionLoading ||
      deployment.status === "success"
    }
    className="bg-green-600 text-white px-5 py-3 rounded-lg hover:bg-green-700 disabled:opacity-50"
  >
    {actionLoading
      ? "Processing..."
      : "Restart Deployment"}
  </button>

</div>


          {/* Container */}

          <div>

            <p className="text-sm text-slate-500">
              Container
            </p>

            <p className="mt-1 font-medium break-all">
              {deployment.container_name ||
                "Not available"}
            </p>

          </div>


          {/* Port */}

          <div>

            <p className="text-sm text-slate-500">
              Host Port
            </p>

            <p className="mt-1 font-medium">
              {deployment.host_port ||
                "Not available"}
            </p>

          </div>


          {/* Started */}

          <div>

            <p className="text-sm text-slate-500">
              Started At
            </p>

            <p className="mt-1 font-medium">
              {deployment.started_at
                ? new Date(
                    deployment.started_at
                  ).toLocaleString()
                : "Not available"}
            </p>

          </div>

        </div>

      </div>


      {/* Deployment Logs */}

      <div className="bg-slate-900 text-white rounded-xl p-6">

        <h2 className="text-lg font-semibold mb-5">
          Deployment Logs
        </h2>


        {logs.length === 0 ? (

          <p className="text-slate-400">
            No deployment logs available.
          </p>

        ) : (

          <div className="space-y-3">

            {logs.map((log) => (

              <div
                key={log.id}
                className="font-mono text-sm"
              >

                <span className="text-slate-400">
                  {log.timestamp
                    ? new Date(
                        log.timestamp
                      ).toLocaleTimeString()
                    : ""}
                </span>

                <span className="ml-4">
                  {log.message}
                </span>

              </div>

            ))}

          </div>

        )}

      </div>

    </div>

  );
}

export default DeploymentDetails;