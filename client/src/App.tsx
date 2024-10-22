import React, { useState } from "react";
import { motion } from "framer-motion";
import clsx from "clsx";
import { LuPin } from "react-icons/lu";
import toast from "react-hot-toast";

import { MdHistory } from "react-icons/md";

function Chip({ children }: { children: React.ReactNode }) {
  return (
    <div className="rounded-full border px-6 cursor-pointer transition-colors text-secondary py-3 font-medium max-lg:px-4 max-lg:text-sm">
      {children}
    </div>
  );
}

const url = "http://localhost:8000/api";

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
      {isOpen && (
        <motion.div
          className="fixed inset-0 bg-black bg-opacity-50 max-lg:hidden"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        />
      )}

      <motion.div
        className="fixed top-0 right-0 h-screen bg-white w-[40vw] shadow-lg z-10 max-lg:hidden"
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

function MobileDrawer({
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
      {isOpen && (
        <motion.div
          className="fixed inset-0 bg-black bg-opacity-50 lg:hidden"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        />
      )}

      <motion.div
        className="fixed bottom-0  bg-white w-screen h-[25vh] shadow-lg z-10 lg:hidden"
        initial={{ y: "100%" }}
        animate={{ y: isOpen ? 0 : "100%" }}
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
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [industry, setIndustry] = useState("");
  const [country, setCountry] = useState("");
  const [_, setReportId] = React.useState<string | null>(null); // Store the report ID
  const [isLoading, setIsLoading] = React.useState<boolean>(false); // Loading state
  const [reportContent, setReportContent] = React.useState<string | null>(null);

  function fetchMarkdownReport(reportId: string) {
    fetch(`${url}/report/markdown/${reportId}`)
      .then((response) => {
        if (response.ok) {
          return response.text();
        } else {
          throw new Error("Failed to fetch report.");
        }
      })
      .then((markdown) => {
        setReportContent(markdown);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching report:", error);
        toast.error("Error fetching report");
        setIsLoading(false);
      });
  }

  function pollReportStatus(reportId: string) {
    const intervalId = setInterval(() => {
      fetch(`${url}/status/${reportId}`)
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "completed") {
            clearInterval(intervalId); // Stop polling
            fetchMarkdownReport(reportId); // Fetch the report content
          } else if (data.status === "not_found") {
            clearInterval(intervalId); // Stop polling if not found
            setIsLoading(false);
          }
        })
        .catch((error) => {
          toast.error("Error checking report status");
          console.error("Error checking report status:", error);
          clearInterval(intervalId);
          setIsLoading(false);
        });
    }, 2000); // Poll every 2 seconds
  }

  function handleReportGeneration() {
    setIsOpen(true);
    setIsLoading(true);
    setReportContent(null);

    fetch(`${url}/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        country: country,
        industry: industry,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "in_progress") {
          setReportId(data.report_id);
          toast.success("Report generation started");
          pollReportStatus(data.report_id);
        } else {
          setIsLoading(false);
        }
      })
      .catch((error) => {
        toast.error(
          "Error starting report generation, check console logs for more information"
        );
        console.error("Error generating report:", error);
        setIsLoading(false);
      });
  }

  return (
    <main className="h-screen grid grid-cols-[14vw_1fr] font-mont relative">
      <aside className="grid grid-rows-[90vh_1fr] border-l max-lg:hidden">
        <main className="flex flex-col px-8 pt-8 border-r">
          <img src="/msbc-logo.png" alt="msbc-logo" className="w-44" />
          <div className="mt-8 font-semibold text-xl flex items-center gap-2">
            Reports
          </div>
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
        <img
          src="/msbc-logo.png"
          alt="msbc-logo"
          className="w-36 p-4 lg:hidden"
        />
        <div className="pl-10 pt-10 flex flex-col mt-20 max-lg:mt-0 max-lg:p-0 max-lg:pl-4">
          <h1 className="text-5xl font-extrabold text-primary max-lg:text-2xl">
            Good Afternoon!
          </h1>
          <p className="mt-3 text-2xl font-medium opacity-70 max-lg:text-lg max-lg:m-0">
            John Doe
          </p>

          <h2 className="mt-16 text-xl font-medium max-lg:mt-12 max-lg:text-base">
            Reports
          </h2>
          <div className="flex gap-4 mt-2 max-lg:overflow-x-scroll max-lg:w-[90vw] max-lg:pr-6">
            <Chip>Healthcare</Chip>
            <Chip>Finance</Chip>
            <Chip>Clothing</Chip>
            <Chip>Crypto</Chip>
          </div>

          <div className="flex mt-8 flex-col border w-fit px-8 py-8 rounded-3xl max-lg:w-[92vw]">
            <h2 className=" text-[#212121] text-2xl max-lg:font-bold">
              Generate a report
            </h2>
            <label className="text-sm font-bold text-secondary mt-4 max-lg:mt-6">
              Industry
            </label>
            <input
              type="text"
              className="border w-[30vw] max-lg:w-full px-4 py-2 rounded-md mt-2 focus:outline-primary"
              placeholder="Healthcare"
              value={industry}
              onChange={(e) => setIndustry(e.target.value)} // Set industry
            />
            <label className="text-sm font-bold text-secondary mt-4">
              Country
            </label>
            <input
              type="text"
              className="border w-[30vw] px-4 py-2 rounded-md mt-2 focus:outline-primary max-lg:w-full"
              placeholder="UAE"
              value={country}
              onChange={(e) => setCountry(e.target.value)} // Set country
            />

            <button
              className="bg-secondary hover:bg-opacity-95 transition-colors text-white mt-4 rounded-full py-3 font-bold disabled:cursor-not-allowed disabled:bg-opacity-25 max-lg:text-sm max-lg:mt-8"
              onClick={handleReportGeneration}
              disabled={industry.trim() === "" || country.trim() === ""}
            >
              Generate Report
            </button>
          </div>
        </div>
      </main>

      <Drawer isOpen={isOpen} onClose={() => setIsOpen(false)}>
        {isLoading && (
          <div className="max-lg:hidden">
            <div className="text-primary font-bold text-2xl mt-2">
              Generating the report
            </div>
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
              className="border font-bold px-8 py-2 rounded-full absolute mt-4 hover:bg-[#f1f1f1] transition-colors"
              onClick={() => setIsOpen(false)}
            >
              Stop Generating
            </button>
          </div>
        )}

        {reportContent && (
          <div className="mt-10 max-lg:hidden">
            <h2 className="text-2xl font-bold">Generated Report</h2>
            <pre className="whitespace-pre-wrap">{reportContent}</pre>
          </div>
        )}
      </Drawer>

      {/* Mobile Drawer */}
      <MobileDrawer isOpen={isOpen} onClose={() => setIsOpen(false)}>
        {isLoading && (
          <div className="lg:hidden">
            <div className="text-primary font-bold text-lg m-0">
              Generating the report
            </div>
            <div className="">
              <Skeleton />
              <Skeleton className="w-96 h-20" />
              <Skeleton className="w-[30px] h-20" />
              <Skeleton className="w-[70px] h-10" />
            </div>
            <button
              className="border font-bold px-8 py-2 rounded-full absolute mt-4 text-sm hover:bg-[#f1f1f1] transition-colors"
              onClick={() => setIsOpen(false)}
            >
              Stop Generating
            </button>
          </div>
        )}

        {reportContent && (
          <div className="mt-10 max-lg:hidden">
            <h2 className="text-2xl font-bold">Generated Report</h2>
            <pre className="whitespace-pre-wrap">{reportContent}</pre>
          </div>
        )}
      </MobileDrawer>
    </main>
  );
}

export default App;
