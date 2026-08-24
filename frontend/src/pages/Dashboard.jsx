import { useEffect, useState } from "react";
import api from "../services/api";

function Dashboard() {

  const [applications, setApplications] =
    useState([]);

  useEffect(() => {

    const fetchApplications = async () => {

      try {

        const response = await api.get(
          "/applications/"
        );

        setApplications(response.data);

      } catch (error) {

        console.error(
          "Failed to fetch applications:",
          error
        );

      }

    };

    fetchApplications();

  }, []);

  return (
    <div>

      <h1>CloudOps Dashboard</h1>

      <h2>
        Applications: {applications.length}
      </h2>

      {applications.map((application) => (

        <div key={application.id}>

          <h3>
            {application.name}
          </h3>

          <p>
            Status: {application.status}
          </p>

          <p>
            Repository:
            {" "}
            {application.repository_url}
          </p>

        </div>

      ))}

    </div>
  );
}

export default Dashboard;