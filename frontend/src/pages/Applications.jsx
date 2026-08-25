import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

function Applications() {

  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

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

  useEffect(() => {
    fetchApplications();
  }, []);

  if (loading) {
    return <p>Loading applications...</p>;
  }

  return (

    <div>

      <div className="flex justify-between items-center mb-8">

        <div>

          <h1 className="text-3xl font-bold">
            Applications
          </h1>

          <p className="text-slate-500 mt-2">
            Manage your deployed applications.
          </p>

        </div>

        <Link
          to="/applications/new"
          className="bg-slate-900 text-white px-5 py-3 rounded-lg hover:bg-slate-800"
        >
          + New Application
        </Link>

      </div>


      <div className="grid gap-5">

        {applications.map((application) => (

          <div
            key={application.id}
            className="bg-white p-6 rounded-xl shadow-sm"
          >

            <div className="flex justify-between">

              <div>

                <h2 className="text-xl font-semibold">
                  {application.name}
                </h2>

                <p className="text-slate-500 mt-2">
                  {application.repository_url}
                </p>

              </div>

              <span className="text-green-600">
                {application.status}
              </span>

            </div>

            <Link
              to={`/applications/${application.id}`}
              className="inline-block mt-4 text-blue-600"
            >
              View application →
            </Link>

          </div>

        ))}

      </div>

    </div>

  );
}

export default Applications;