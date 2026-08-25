import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Applications from "./pages/Applications";
import CreateApplication from "./pages/CreateApplication";
import ApplicationDetails from "./pages/ApplicationDetails";
import Deployments from "./pages/Deployments";
import DeploymentDetails from "./pages/DeploymentDetails";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import Layout from "./components/Layout";

function App() {
  return (
    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Navigate to="/login" />}
        />

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Layout>
                <Dashboard />
              </Layout>
            </ProtectedRoute>
          }
        />
        <Route
  path="/applications"
  element={
    <ProtectedRoute>
      <Layout>
        <Applications />
      </Layout>
    </ProtectedRoute>
  }
/>

<Route
  path="/applications/new"
  element={
    <ProtectedRoute>
      <Layout>
        <CreateApplication />
      </Layout>
    </ProtectedRoute>
  }
/>
      
      <Route
  path="/applications/:id"
  element={
    <ProtectedRoute>
      <Layout>
        <ApplicationDetails />
      </Layout>
    </ProtectedRoute>
  }
/>    
      <Route
  path="/deployments"
  element={
    <ProtectedRoute>
      <Layout>
        <Deployments />
      </Layout>
    </ProtectedRoute>
  }
/>
     <Route
  path="/deployments/:id"
  element={
    <ProtectedRoute>
      <Layout>
        <DeploymentDetails />
      </Layout>
    </ProtectedRoute>
  }
/>

      </Routes>

      
      

    </BrowserRouter>
  );
}

export default App;