
import "./App.css";
import HomeNav from "./components/HomeNav";


function App() {
  return (
    <>
      <HomeNav />
      <h1 className="welcome">Welcome to Savash</h1>
      <h2 className="welcome">The note taking and assignment submission app</h2>
      {Array.from({ length: 200 }).map((_, i) => (<br key={i} />))}
      <button>Secret</button>
    </>
  );
}

export default App;
