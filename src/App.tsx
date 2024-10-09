import React from "react";
import { motion } from "framer-motion";
import clsx from "clsx";
import { LuPin } from "react-icons/lu";
import { IoDocument } from "react-icons/io5";
import { MdHistory } from "react-icons/md";

function Chip({ children }: { children: React.ReactNode }) {
  return (
    <div className="rounded-full bg-primary/90 hover:bg-primary cursor-pointer transition-colors text-white px-4 py-2 font-medium">
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
  const [docs, setDocs] = React.useState<any>(["In father we trust", "Meow Meow Meow"]);

  return (
    <main className="h-screen grid grid-cols-[14vw_1fr] font-mont relative">
      <aside className="grid grid-rows-[92vh_1fr] border-l">
        <main className="flex flex-col px-8 pt-8 border-r">
          <img src="/msbc-logo.png" alt="msbc-logo" className="w-44" />
          <div className="mt-8 font-medium text-xl flex items-center gap-2">
            Reports
            <IoDocument />
          </div>
          <div className="mt-8 font-bold opacity-75 flex items-center gap-2">
            Pinned <LuPin />
          </div>
          {
            pinnedDocs.map((p: any) => (<div className="opacity-80 hover:opacity-100 transition-opacity cursor-pointer truncate w-[10vw]">{p}</div>))
          }
          <div className="mt-8 font-bold opacity-75 flex items-center gap-2">
            History <MdHistory />
          </div>
          {
            docs.map((p: any) => (<div className="opacity-80 hover:opacity-100 transition-opacity cursor-pointer truncate w-[10vw]">{p}</div>))
          }
        </main>
        <main className=" border-t border-r flex justify-center items-center">
          <div className="bg-primary w-56 p-2 rounded-lg text-white flex items-center gap-4">
            <div className="bg-white size-8 rounded-full"></div>
            <p className="font-medium">Janmejay Chat</p>
          </div>
        </main>
      </aside>
      <main className="grid grid-rows-[8vh_1fr]">
        <div className="border-b flex items-center pl-10">
          <p className="text-primary font-bold text-3xl">Research Room</p>
        </div>
        <div className="pl-10 pt-10 flex flex-col">
          <h1 className="text-5xl font-bold text-primary">Good Morning!</h1>
          <p className="mt-3 text-2xl font-medium opacity-70">
            Janmejay Chatterjee
          </p>

          <h2 className="mt-16 text-primary font-bold text-3xl">Reports</h2>
          <div className="flex gap-4 mt-6">
            <Chip>Healthcare</Chip>
            <Chip>Finance</Chip>
            <Chip>Clothing</Chip>
            <Chip>Crypto</Chip>
          </div>

          <h2 className="mt-16 text-primary font-bold text-3xl">Generate Report</h2>
          <div className="flex mt-6 flex-col border w-[20vw] px-8 py-4 rounded-md">

            <label className="text-xl font-bold text-primary">Industry</label>
            <input
              type="text"
              className="border w-full px-4 py-2 rounded-md mt-2 focus:outline-primary"
              placeholder="Healthcare"
            />
            <label className="text-xl font-bold text-primary mt-2">
              Country
            </label>
            <input
              type="text"
              className="border w-full px-4 py-2 rounded-md mt-2 focus:outline-primary"
              placeholder="UAE"
            />

            <button
              className="bg-primary/90 hover:bg-primary transition-colors text-white mt-4 rounded-full py-3 font-bold"
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
