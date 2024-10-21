import React from "react";
import { motion } from "framer-motion";
import clsx from "clsx";
import { LuPin } from "react-icons/lu";
import { IoDocument } from "react-icons/io5";
import { MdHistory } from "react-icons/md";

function Chip({ children }: { children: React.ReactNode }) {
  return (
    <div className="rounded-full border px-6 cursor-pointer transition-colors text-secondary py-3 font-medium">
      {children}
    </div>
  );
}

function Drawer({
  children,
  isOpen,
  onClose,
}: {
  children: React.ReactNode;
  isOpen: boolean;
  onClose: () => void;
}) {
  return (
    <>
      {/* Background Overlay */}
      {isOpen && (
        <motion.div
          className="fixed inset-0 bg-black bg-opacity-50 "
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose} // Close the drawer if clicked on the overlay
        />
      )}

      {/* Drawer Content */}
      <motion.div
        className="fixed top-0 right-0 h-screen bg-white w-[40vw] shadow-lg z-10"
        initial={{ x: "100%" }}
        animate={{ x: isOpen ? 0 : "100%" }}
        transition={{ type: "spring", stiffness: 300, damping: 30 }}
      >
        <div className="p-4 relative">
          <button
            className="absolute top-2 right-2 text-white font-bold"
            onClick={onClose}
          >
            X
          </button>
          {children}
        </div>
      </motion.div>
    </>
  );
}

function Skeleton({ className }: { className?: string }) {
  return (
    <div
      className={clsx(
        className,
        "bg-gray-400 w-36 h-4 animate-pulse rounded-sm my-2"
      )}
    ></div>
  );
}

function App() {
  const [isOpen, setIsOpen] = React.useState<boolean>(false);
  const [pinnedDocs, setPinnedDocs] = React.useState<any>([
    "Lorem ipsum john doe hello world",
    "meow meow meow",
  ]);
  const [docs, setDocs] = React.useState<any>([
    "In father we trust",
    "Meow Meow Meow",
  ]);

  return (
    <main className="h-screen grid grid-cols-[14vw_1fr] font-mont relative">
      <aside className="grid grid-rows-[90vh_1fr] border-l">
        <main className="flex flex-col px-8 pt-8 border-r">
          <img src="/msbc-logo.png" alt="msbc-logo" className="w-44" />
          <div className="mt-8 font-semibold text-xl flex items-center gap-2">
            Reports
          </div>
          <div className="mt-8 font-bold opacity-75 flex items-center gap-2 mb-2">
            <LuPin /> Pinned
          </div>
          {pinnedDocs.map((p: any) => (
            <div className="transition-all cursor-pointer truncate text-xs w-[10vw] bg-[#f8f8f8] hover:bg-[#e2e2e2] mb-2 px-2.5 py-2 ">
              {p}
            </div>
          ))}
          <div className="mt-8 font-bold opacity-75 flex items-center gap-2 mb-2">
            <MdHistory /> History
          </div>
          {docs.map((p: any) => (
            <div className=" transition-all cursor-pointer truncate text-xs w-[10vw] bg-[#f8f8f8] hover:bg-[#e2e2e2] mb-2 px-2.5 py-2">
              {p}
            </div>
          ))}
        </main>
        <main className="border-r flex justify-center items-center">
          <div className="bg-secondary bg-opacity-10 w-56 p-2 rounded-lg text-white flex items-center gap-4">
            <div className="size-8 rounded-full bg-secondary"></div>
            <div>
              <p className="font-semibold text-black">John Doe</p>
              <p className="text-xs text-black">Manager</p>
            </div>
          </div>
        </main>
      </aside>
      <main className="grid grid-rows-[8vh_1fr]">
        <div className="pl-10 pt-10 flex flex-col mt-20">
          <h1 className="text-5xl font-extrabold text-primary">
            Good Afternoon!
          </h1>
          <p className="mt-3 text-2xl font-medium opacity-70">John Doe</p>

          <h2 className="mt-16 text-xl font-medium">Reports</h2>
          <div className="flex gap-4 mt-2">
            <Chip>Healthcare</Chip>
            <Chip>Finance</Chip>
            <Chip>Clothing</Chip>
            <Chip>Crypto</Chip>
          </div>

          <div className="flex mt-8 flex-col border w-fit px-8 py-8  rounded-3xl">
            <h2 className=" text-[#212121] text-2xl">Generate a report</h2>
            <label className="text-sm font-bold text-secondary mt-4">
              Industry
            </label>
            <input
              type="text"
              className="border w-[30vw] px-4 py-2 rounded-md mt-2 focus:outline-primary"
              placeholder="Healthcare"
            />
            <label className="text-sm font-bold text-secondary mt-4">
              Country
            </label>
            <input
              type="text"
              className="border w-[30vw] px-4 py-2 rounded-md mt-2 focus:outline-primary"
              placeholder="UAE"
            />

            <button
              className="bg-secondary hover:bg-opacity-85 transition-colors text-white mt-4 rounded-full py-3 font-bold"
              onClick={() => setIsOpen(true)}
            >
              Generate Report
            </button>
          </div>
        </div>
      </main>

      <Drawer isOpen={isOpen} onClose={() => setIsOpen(false)}>
        <div className="text-primary font-bold text-2xl">Generating Report</div>
        <div className="mt-10">
          <Skeleton />
          <Skeleton className="w-96 h-20" />
          <Skeleton className="w-[600px] h-20" />
          <Skeleton className="w-[600px] h-10" />
          <Skeleton className="w-[200px] h-20" />
          <Skeleton className="w-[400px] h-20" />
          <Skeleton className="w-[600px] h-20" />
        </div>
        <button
          className="bg-red-500 text-white font-bold px-4 py-2 rounded-full absolute mt-2"
          onClick={() => setIsOpen(false)}
        >
          Cancel
        </button>
      </Drawer>
    </main>
  );
}

export default App;
