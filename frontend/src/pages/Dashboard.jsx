import { useEffect, useState } from "react";
import api from "../services/api";

function Dashboard() {

  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    const fetchApplications = async () => {

      try {

        const response = await api.get(
          "/applications/"
        );

        setApplications(response.data);

      } catch (error) {

        console.error(error);

      } finally {

        setLoading(false);

      }

    };

    fetchApplications();

  }, []);

  if (loading) {
    return <p>Loading dashboard...</p>;
  }

  return (

    <div>

      <div className="mb-8">

        <h1 className="text-3xl font-bold text-slate-900">
          Dashboard
        </h1>

        <p className="text-slate-500 mt-2">
          Monitor your applications and deployments.
        </p>

      </div>


      {/* Statistics */}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">

        <div className="bg-white rounded-xl p-6 shadow-sm">

          <p className="text-slate-500">
            Applications
          </p>

          <p className="text-3xl font-bold mt-2">
            {applications.length}
          </p>

        </div>


        <div className="bg-white rounded-xl p-6 shadow-sm">

          <p className="text-slate-500">
            Deployments
          </p>

          <p className="text-3xl font-bold mt-2">
            0
          </p>

        </div>


        <div className="bg-white rounded-xl p-6 shadow-sm">

          <p className="text-slate-500">
            System Status
          </p>

          <p className="text-3xl font-bold text-green-600 mt-2">
            Healthy
          </p>

        </div>

      </div>


      {/* Applications */}

      <div className="bg-white rounded-xl shadow-sm p-6">

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

                <div className="flex justify-between">

                  <h3 className="font-semibold">
                    {application.name}
                  </h3>

                  <span className="text-green-600">
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

    </div>

  );
}

export default Dashboard;