export default function MarqueeTicker() {
  const allItems = [
    "Find and book your dream apartment online  no office visits needed.",
    "See clear prices and rent durations upfront  no hidden charges.",
    "Submit apartment requests in just a few clicks.",
    "Upload your payment proof securely inside your dashboard.",
    "Track your approval status in real time  no confusion.",
    "Manage all your bookings and payments in one place.",
    "Enjoy a smooth experience on mobile, tablet, or desktop.",
    "Deal directly with the cooperative no middlemen involved.",
    "Access affordable housing options with flexible plans.",
    "Be part of a trusted community building a better future together.",
  ];

  const row1 = allItems.slice(0, 5);
  const row2 = allItems.slice(5, 10);

  const MarqueeRow = ({ items, direction = "left", speed = 30 }) => {
    const doubled = [...items, ...items];
    const animationName = direction === "left" ? "scrollLeft" : "scrollRight";

    return (
      <div className="overflow-hidden flex w-full">
        <div
          className="flex gap-8 whitespace-nowrap will-change-transform"
          style={{
            animation: `${animationName} ${speed}s linear infinite`,
          }}
        >
          {doubled.map((item, i) => (
            <span
              key={i}
              className="inline-flex items-center gap-2.5 text-base font-medium text-gray-800 shrink-0"
            >
              <span className="text-[#FF7D00] text-xl">●</span>
              {item}
            </span>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="py-8 flex flex-col gap-5">
      <style>{`
        @keyframes scrollLeft {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        @keyframes scrollRight {
          0% { transform: translateX(-50%); }
          100% { transform: translateX(0); }
        }
      `}</style>

      <MarqueeRow items={row1} direction="left" speed={37} />
      <MarqueeRow items={row2} direction="right" speed={37} />
    </div>
  );
}