import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";

function DeploymentDetails() {

  const { id } = useParams();

  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    const fetchLogs = async () => {

      try {

        const response = await api.get(
          `/deployments/${id}/logs`
        );

        setLogs(response.data);

      } catch (error) {

        console.error(
          "Failed to fetch logs:",
          error
        );

      } finally {

        setLoading(false);

      }

    };

    fetchLogs();

  }, [id]);


  if (loading) {
    return (
      <p>
        Loading deployment logs...
      </p>
    );
  }


  return (

    <div>

      <h1 className="text-3xl font-bold mb-8">
        Deployment #{id}
      </h1>

      <div className="bg-slate-900 text-white rounded-xl p-6">

        <h2 className="text-lg font-semibold mb-5">
          Deployment Logs
        </h2>

        <div className="space-y-3">

          {logs.map((log) => (

            <div
              key={log.id}
              className="font-mono text-sm"
            >

              <span className="text-slate-400">
                {log.timestamp}
              </span>

              <span className="ml-4">
                {log.message}
              </span>

            </div>

          ))}

        </div>

      </div>

    </div>

  );
}

export default DeploymentDetails;