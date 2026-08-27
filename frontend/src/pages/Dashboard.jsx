import { useEffect, useState } from "react";
import api from "../services/api";

function Dashboard() {
  const [applications, setApplications] = useState([]);
  const [deployments, setDeployments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [applicationsResponse, deploymentsResponse] =
          await Promise.all([
            api.get("/applications/"),
            api.get("/deployments/"),
          ]);

        setApplications(applicationsResponse.data);
        setDeployments(deploymentsResponse.data);
      } catch (error) {
        console.error(
          "Failed to load dashboard:",
          error
        );

        setError(
          error.response?.data?.detail ||
            "Failed to load dashboard data."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  // Deployment statistics
  const runningDeployments = deployments.filter(
    (deployment) =>
      deployment.status === "success"
  ).length;

  const stoppedDeployments = deployments.filter(
    (deployment) =>
      deployment.status === "stopped"
  ).length;

  if (loading) {
    return (
      <div className="p-8">
        <p className="text-slate-500">
          Loading dashboard...
        </p>
      </div>
    );
  }

  return (
    <div>
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">
          Dashboard
        </h1>

        <p className="text-slate-500 mt-2">
          Monitor your applications and deployments.
        </p>
      </div>

      {/* Error */}
      {error && (
        <div className="mb-6 rounded-lg bg-red-50 border border-red-200 p-4 text-red-700">
          {error}
        </div>
      )}

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">

        {/* Applications */}
        <div className="bg-white rounded-xl p-6 shadow-sm">
          <p className="text-slate-500">
            Applications
          </p>

          <p className="text-3xl font-bold mt-2">
            {applications.length}
          </p>
        </div>

        {/* Deployments */}
        <div className="bg-white rounded-xl p-6 shadow-sm">
          <p className="text-slate-500">
            Deployments
          </p>

          <p className="text-3xl font-bold mt-2">
            {deployments.length}
          </p>
        </div>

        {/* Running */}
        <div className="bg-white rounded-xl p-6 shadow-sm">
          <p className="text-slate-500">
            Running
          </p>

          <p className="text-3xl font-bold text-green-600 mt-2">
            {runningDeployments}
          </p>
        </div>

        {/* Stopped */}
        <div className="bg-white rounded-xl p-6 shadow-sm">
          <p className="text-slate-500">
            Stopped
          </p>

          <p className="text-3xl font-bold text-red-600 mt-2">
            {stoppedDeployments}
          </p>
        </div>

      </div>

      {/* System Status */}
      <div className="bg-white rounded-xl shadow-sm p-6 mb-8">

        <div className="flex justify-between items-center">

          <div>
            <h2 className="text-xl font-semibold">
              System Status
            </h2>

            <p className="text-slate-500 mt-1">
              CloudOps API and dashboard connection
            </p>
          </div>

          <span className="px-4 py-2 rounded-full bg-green-100 text-green-700 font-medium">
            Healthy
          </span>

        </div>

      </div>

      {/* Applications */}
      <div className="bg-white rounded-xl shadow-sm p-6 mb-8">

        <h2 className="text-xl font-semibold mb-5">
          Applications
        </h2>

        {applications.length === 0 ? (

          <p className="text-slate-500">
            No applications yet.
          </p>

        ) : (

          <div className="space-y-4">

            {applications.map((application) => (

              <div
                key={application.id}
                className="border rounded-lg p-4"
              >

                <div className="flex justify-between items-center">

                  <h3 className="font-semibold">
                    {application.name}
                  </h3>

                  <span
                    className={
                      application.status === "built"
                        ? "text-green-600"
                        : application.status === "failed"
                        ? "text-red-600"
                        : "text-yellow-600"
                    }
                  >
                    {application.status}
                  </span>

                </div>

                <p className="text-sm text-slate-500 mt-2">
                  {application.repository_url}
                </p>

              </div>

            ))}

          </div>

        )}

      </div>

      {/* Recent Deployments */}
      <div className="bg-white rounded-xl shadow-sm p-6">

        <h2 className="text-xl font-semibold mb-5">
          Recent Deployments
        </h2>

        {deployments.length === 0 ? (

          <p className="text-slate-500">
            No deployments yet.
          </p>

        ) : (

          <div className="space-y-4">

            {deployments
              .slice()
              .reverse()
              .slice(0, 5)
              .map((deployment) => (

                <div
                  key={deployment.id}
                  className="border rounded-lg p-4 flex flex-col md:flex-row md:items-center md:justify-between gap-3"
                >

                  <div>

                    <h3 className="font-semibold">
                      Deployment #{deployment.id}
                    </h3>

                    <p className="text-sm text-slate-500 mt-1">
                      Application ID:{" "}
                      {deployment.application_id}
                    </p>

                    <p className="text-sm text-slate-500 mt-1">
                      Version: {deployment.version}
                    </p>

                  </div>

                  <span
                    className={
                      deployment.status === "success"
                        ? "px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-700"
                        : deployment.status === "stopped"
                        ? "px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-700"
                        : deployment.status === "failed"
                        ? "px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-700"
                        : "px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-700"
                    }
                  >
                    {deployment.status}
                  </span>

                </div>

              ))}

          </div>

        )}

      </div>

    </div>
  );
}

export default Dashboard;