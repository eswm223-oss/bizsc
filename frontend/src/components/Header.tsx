import { Link } from "react-router-dom";

function Header() {
  return (
    <header className="navbar navbar-dark bg-dark px-4">
      <Link className="navbar-brand" to="/">
        BizSC
      </Link>

      <nav className="d-flex gap-3">
        <Link className="nav-link text-white" to="/">
          Home
        </Link>

        <Link className="nav-link text-white" to="/users">
          Users
        </Link>
      </nav>
    </header>
  );
}

export default Header;
