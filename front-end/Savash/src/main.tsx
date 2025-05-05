import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import Register from './Register.tsx'
import Login from './Login.tsx'
import CreateClass from './CreateClass.tsx'
import Dashboard from './Dashboard.tsx'
import Join from './Join.tsx'

import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Classes from './Classes.tsx'
import Inbox from './Inbox.tsx'

//https://www.youtube.com/watch?v=oTIJunBa6MA&ab_channel=CosdenSolutions

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: (
      <div>
        404 Not Found{" "}
        <a href="/">
          <button>Home</button>
        </a>
      </div>
    ),
  },
  {
    path: "/register",
    element: <Register />,
  },
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/classes",
    element: <Classes />,
  },
  {
    path: "/create",
    element: <CreateClass />
  },
  {
    path: "/dashboard",
    element: <Dashboard />
  },
  {
    path: "/join",
    element: <Join />
  },
  {
    path: "/inbox",
    element: <Inbox />
  }
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
