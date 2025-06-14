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
import Class from './Class.tsx'
import AddAssignment from './AddAssignment.tsx'
import Contact from './Contact.tsx'
import Assignment from './Assignment.tsx'
import Theme from './Theme.tsx'
import Game from './Game.tsx'

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
    element: <CreateClass />,
  },
  {
    path: "/dashboard",
    element: <Dashboard />,
  },
  {
    path: "/join",
    element: <Join />,
  },
  {
    path: "/theme",
    element: <Theme />,
  },
  {
    path: "/inbox",
    element: <Inbox />,
  },
  {
    path: "/class/:id",
    element: <Class />,
  },
  {
    path: "/class/:id/add",
    element: <AddAssignment />,
  },
  {
    path: "/contact",
    element: <Contact />,
  },
  {
    path: "/class/:classid/assignment/:assignmentid",
    element: <Assignment />,
  },
  {
    path: "/game",
    element: <Game />,
  },
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
