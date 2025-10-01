/// src/components/FormNYSC.jsx
import React, { useState } from "react";
import { toast } from "react-toastify";

const FormNYSC = ({ onSubmit, isLoading }) => {
  const [callupNo, setCallupNo] = useState("");
  const [certificateNo, setCertificateNo] = useState("");
  const [dob, setDob] = useState("");

  const inputClassName =
    "mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500";

  const validateForm = () => {
    const errors = [];
    if (!callupNo) errors.push("Call-Up Number");
    if (!certificateNo) errors.push("Certificate Number");
    if (!dob) errors.push("Date of Birth");
    if (errors.length === 0) return true;

    toast.error(`Please fill: ${errors.join(", ")}`);
    return false;
  };
  
  const handleSubmit = (event) => {
    event.preventDefault();
    if (!validateForm()) return;

    const formData = {
      callup_no: callupNo,
      certificate_no: certificateNo,
      dob,
    };

    toast.success("Request sent!");
    onSubmit(event, formData, "NYSC");
  };

  return (
    <form onSubmit={handleSubmit} noValidate className="p-6 space-y-6">
      <div>
        <label
          htmlFor="callupNo"
          className="block text-sm font-bold text-gray-800 mb-1"
        >
          Call-Up Number*
        </label>
        <input
          type="text"
          id="callupNo"
          value={callupNo}
          onChange={(e) => setCallupNo(e.target.value)}
          placeholder="e.g. NYSC2025ABC123"
          required
          className={inputClassName}
        />
      </div>

      <div>
        <label
          htmlFor="certificateNo"
          className="block text-sm font-bold text-gray-800 mb-1"
        >
          Certificate Number*
        </label>
        <input
          type="text"
          id="certificateNo"
          value={certificateNo}
          onChange={(e) => setCertificateNo(e.target.value)}
          placeholder="e.g. CERT56789"
          required
          className={inputClassName}
        />
      </div>

      <div>
        <label
          htmlFor="dob"
          className="block text-sm font-bold text-gray-800 mb-1"
        >
          Date of Birth*
        </label>
        <input
          type="date"
          id="dob"
          value={dob}
          onChange={(e) => setDob(e.target.value)}
          required
          className={inputClassName}
        />
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className={`
          relative w-full px-6 py-4 rounded-lg font-semibold text-base
          transition-all duration-300 ease-in-out
          focus:outline-none focus:ring-4 focus:ring-emerald-500/50
          transform hover:-translate-y-0.5 active:translate-y-0
          disabled:cursor-not-allowed disabled:transform-none
          ${
            isLoading
              ? "bg-emerald-600/80 text-emerald-100"
              : "bg-emerald-600 text-white hover:bg-emerald-700 active:bg-emerald-800"
          }
          shadow-lg hover:shadow-xl active:shadow-md
          overflow-hidden
        `}
      >
        {isLoading ? "Validating..." : "Verify NYSC"}
      </button>
    </form>
  );
};

export default FormNYSC;
