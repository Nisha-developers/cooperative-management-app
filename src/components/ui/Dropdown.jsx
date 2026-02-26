import React, { useState, useRef, useEffect } from "react";
import { FaCaretDown } from "react-icons/fa";

const Dropdown = ({ label, items, onOpen, isMobile }) => {
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Close when clicking outside
  useEffect(() => {
    function handleClickOutside(e) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleToggle = () => {
    if (!open && onOpen) {
      onOpen();
    }
    setOpen(!open);
  };

  // ─── MOBILE ───
  if (isMobile) {
    return (
      <div ref={dropdownRef} className="w-full">
        <button
          onClick={handleToggle}
          className="block w-full px-4 py-3.5 rounded-xl text-[15px] font-medium
            transition-all duration-300 ease-out
            text-cooperative-dark/75 hover:bg-cooperative-dark/5
            hover:text-cooperative-dark hover:translate-x-1"
        >
          <span className="flex items-center justify-between">
            <span className="flex items-center gap-3">
              <span className="w-1.5 h-1.5 rounded-full bg-cooperative-dark/20" />
              {label}
            </span>
            <FaCaretDown
              className={`text-cooperative-dark/40 transition-transform duration-300
                ${open ? "rotate-180" : "rotate-0"}`}
            />
          </span>
        </button>

        <div
          className={`overflow-hidden transition-all duration-300 ease-in-out
            ${open ? "max-h-60 opacity-100" : "max-h-0 opacity-0"}`}
        >
          <div className="ml-7 mr-3 mb-2 flex flex-col border-l-2 border-cooperative-dark/10 pl-4">
            {items.map((item) => (
              <a
                key={item.href}
                href={item.href}
                onClick={() => setOpen(false)}
                className="py-2.5 text-[14px] font-medium text-cooperative-dark/65
                  hover:text-cooperative-teal transition-colors duration-200"
              >
                {item.label}
              </a>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // ─── DESKTOP ───
  return (
    <div ref={dropdownRef} className="relative">
      <button
        onClick={handleToggle}
        className={`relative flex items-center px-3 py-2 text-sm font-medium rounded-lg
          transition-all duration-300 ease-out text-cooperative-cream
          hover:bg-cooperative-cream/10 before:content-[''] before:absolute before:bottom-0 before:left-1/2
          before:-translate-x-1/2 before:h-[2px] before:rounded-full
          before:bg-cooperative-orange before:transition-all before:duration-300 hover:text-cooperative-orange
          ${open ? "before:w-0 hover:before:w-0" : "before:w-0 hover:before:w-[60%]"}`}
      >
        {label}
        <FaCaretDown
          className={`ml-1 transition-transform duration-300 ${
            open ? "rotate-180" : ""
          }`}
        />
      </button>

      <div
        className={`absolute left-0 mt-2 w-48 bg-white rounded-lg shadow-lg transition-all duration-300
          ${open ? "opacity-100 translate-y-0" : "opacity-0 -translate-y-2 pointer-events-none"}`}
      >
        {items.map((item) => (
          <a
            key={item.href}
            href={item.href}
            className="block px-4 py-2 text-sm hover:bg-gray-100"
            onClick={() => setOpen(false)}
          >
            {item.label}
          </a>
        ))}
      </div>
    </div>
  );
};

export default Dropdown;