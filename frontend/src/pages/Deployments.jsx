import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

function Deployments() {
  const [deployments, setDeployments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDeployments = async () => {
      try {
        const response = await api.get("/deployments/");

        setDeployments(response.data);
      } catch (error) {
        console.error(
          "Failed to fetch deployments:",
          error
        );

        setError("Failed to load deployments.");
      } finally {
        setLoading(false);
      }
    };

    fetchDeployments();
  }, []);

  // Loading state
  if (loading) {
    return (
      <div className="p-8">
        <p className="text-slate-500">
          Loading deployments...
        </p>
      </div>
    );
  }

  return (
    <div>
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">
          Deployments
        </h1>

        <p className="text-slate-500 mt-2">
          Monitor application deployments and deployment logs.
        </p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 rounded-lg bg-red-50 border border-red-200 p-4 text-red-700">
          {error}
        </div>
      )}

      {/* Deployments Container */}
      <div className="bg-white rounded-xl shadow-sm overflow-hidden">

        {deployments.length === 0 ? (
          <div className="p-8 text-center">

            <h2 className="text-lg font-semibold text-slate-700">
              No deployments yet
            </h2>

            <p className="text-slate-500 mt-2">
              Deploy an application to see its deployment here.
            </p>

            <Link
              to="/applications"
              className="inline-block mt-5 bg-slate-900 text-white px-5 py-3 rounded-lg hover:bg-slate-800"
            >
              View Applications
            </Link>

          </div>
        ) : (
          <div className="divide-y">

            {deployments.map((deployment) => (
              <div
                key={deployment.id}
                className="p-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4"
              >

                {/* Deployment Information */}
                <div>

                  <p className="text-lg font-semibold text-slate-900">
                    Deployment #{deployment.id}
                  </p>

                  <p className="text-sm text-slate-500 mt-1">
                    Application ID:{" "}
                    {deployment.application_id}
                  </p>

                  <p className="text-sm text-slate-500 mt-1">
                    Version:{" "}
                    {deployment.version}
                  </p>

                  {deployment.started_at && (
                    <p className="text-sm text-slate-400 mt-1">
                      Started:{" "}
                      {new Date(
                        deployment.started_at
                      ).toLocaleString()}
                    </p>
                  )}

                </div>


                {/* Status + Logs */}
                <div className="flex items-center gap-5">

                  {/* Status */}
                  <span
                    className={
                      deployment.status === "success"
                        ? "px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-700"
                        : deployment.status === "failed"
                        ? "px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-700"
                        : "px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-700"
                    }
                  >
                    {deployment.status}
                  </span>


                  {/* View Logs */}
                  <Link
                    to={`/deployments/${deployment.id}`}
                    className="text-blue-600 font-medium hover:underline"
                  >
                    View Logs →
                  </Link>

                </div>

              </div>
            ))}

          </div>
        )}

      </div>
    </div>
  );
}

export default Deployments;