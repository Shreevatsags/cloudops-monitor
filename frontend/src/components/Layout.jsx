import { Link, useNavigate } from "react-router-dom";

function Layout({ children }) {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-slate-50">

      <div className="flex min-h-screen">

        {/* Sidebar */}
        <aside className="w-64 bg-slate-900 text-white p-6">

          <h1 className="text-2xl font-bold mb-8">
            CloudOps
          </h1>

          <nav className="space-y-2">

            <Link
              to="/dashboard"
              className="block rounded-lg px-4 py-3 hover:bg-slate-800"
            >
              Dashboard
            </Link>

            <Link
              to="/applications"
              className="block rounded-lg px-4 py-3 hover:bg-slate-800"
            >
              Applications
            </Link>

            <Link
              to="/deployments"
              className="block rounded-lg px-4 py-3 hover:bg-slate-800"
            >
              Deployments
            </Link>

          </nav>

          <button
            onClick={logout}
            className="mt-10 w-full rounded-lg bg-red-600 px-4 py-3 hover:bg-red-700"
          >
            Logout
          </button>

        </aside>

        {/* Main content */}
        <main className="flex-1 p-8">
          {children}
        </main>

      </div>

    </div>
  );
}

export default Layout;