import { useEffect, useState } from "react";
import api from "../services/api";

function Deployments() {
  const [deployments, setDeployments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDeployments = async () => {
      try {
        const response = await api.get(
          "/deployments/"
        );

        setDeployments(response.data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchDeployments();
  }, []);

  if (loading) {
    return <p>Loading deployments...</p>;
  }

  return (
    <div>

      <h1 className="text-3xl font-bold mb-8">
        Deployments
      </h1>

      <div className="bg-white rounded-xl shadow-sm">

        {deployments.length === 0 ? (
          <div className="p-6 text-slate-500">
            No deployments yet.
          </div>
        ) : (
          <div className="divide-y">

            {deployments.map((deployment) => (
              <div
                key={deployment.id}
                className="p-6 flex justify-between"
              >

                <div>
                  <p className="font-semibold">
                    Deployment #{deployment.id}
                  </p>

                  <p className="text-slate-500">
                    Version: {deployment.version}
                  </p>
                </div>

                <span>
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

export default Deployments;