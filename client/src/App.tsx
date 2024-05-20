import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Home, AboutPage } from "./pages";
import ErrorPage from "./pages/error-page";

function App() {
  const router = createBrowserRouter([
    { path: "/", element: <Home />, errorElement: <ErrorPage /> },
    { path: "/home", element: <Home />, errorElement: <ErrorPage /> },
    {
      path: "/about",
      element: <AboutPage />,
      errorElement: <ErrorPage />,
    },
  ]);

  return <RouterProvider router={router} />;
}

export default App;