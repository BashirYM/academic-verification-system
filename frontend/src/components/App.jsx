import React, { useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Modal from './Modal';
import ResultComponent from './ResultComponents';
import Form from './Form';
import FormNYSC from './FormNYSC'; // 👈 new NYSC form

function App() {
  const [result, setResult] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedForm, setSelectedForm] = useState('WAEC');

  const WAECExamTypeOptions = {
    1: 'MAY/JUN',
    2: 'NOV/DEC',
  };

  const NECOExamTypeOptions = {
    1: 'ssce_int',
    2: 'ssce_ext',
    3: 'ncee',
    4: 'bece',
    5: 'gifted',
  };

  const subjectsList = [
    'MATHEMATICS',
    'ENGLISH LANGUAGE',
    'BIOLOGY',
    'CHEMISTRY',
    'PHYSICS',
    'GEOGRAPHY',
    'HISTORY',
    'ECONOMICS',
    'GOVERNMENT',
    'LITERATURE',
    'AGRICULTURAL SCIENCE',
    'COMPUTER STUDIES',
    'CIVIC EDUCATION',
    'DATA PROCESSING',
    'MARKETING',
    'ISLAMIC STUDIES',
    'CHRISTIAN RELIGIOUS STUDIES',
    'CATERING CRAFT PRACTICE',
  ].sort();

  const handleSubmit = async (event, formData, formType) => {
    event.preventDefault();
    setResult(null);
    setIsLoading(true);

    let url;
    if (formType === 'WAEC') {
      url = 'http://localhost:5000/api/waec';
    } else if (formType === 'NECO') {
      url = 'http://localhost:5000/api/neco';
    } else if (formType === 'NYSC') {
      url = 'http://localhost:5000/api/nysc';
    }

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      setResult(data);
      setIsModalOpen(true);
    } catch (err) {
      toast.error('Verification failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-emerald-800">
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="flex flex-col md:flex-row">
            {/* Left side instructions */}
            <div className="w-full md:w-2/5 bg-emerald-800 text-white p-8">
              <h2 className="text-3xl font-bold mb-6">CREDLY RESULTS</h2>
              <h3 className="text-xl font-semibold mb-4">How it works:</h3>
              <ul className="list-disc list-inside space-y-2">
                <li>Choose WAEC, NECO, or NYSC verification.</li>
                <li>Fill in the required details in the form.</li>
                <li>Click on the &ldquo;Verify Result&rdquo; button.</li>
                <li>View your verified result.</li>
              </ul>
              <div className="mt-8 flex items-center space-x-4">
                <svg
                  width="52"
                  height="52"
                  viewBox="0 0 52 52"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M25.9998 0.166504C11.7398 0.166504 0.166504 11.7398 0.166504 25.9998C0.166504 40.2598 11.7398 51.8332 25.9998 51.8332C40.2598 51.8332 51.8332 40.2598 51.8332 25.9998C51.8332 11.7398 40.2598 0.166504 25.9998 0.166504ZM39.5623 28.0923C39.5623 28.5315 39.5365 28.9448 39.4848 29.3582C39.0973 33.9307 36.3848 36.204 31.4248 36.204H30.7532C30.3398 36.204 29.9265 36.4107 29.6682 36.7465L27.6273 39.459C26.7232 40.6732 25.2765 40.6732 24.3723 39.459L22.3315 36.7465C22.099 36.4623 21.6082 36.204 21.2465 36.204H20.5748C15.1757 36.204 12.4373 34.8607 12.4373 28.0665V21.2723C12.4373 16.3123 14.7365 13.5998 19.2832 13.2123C19.6965 13.1865 20.1357 13.1865 20.5748 13.1865H31.4248C36.824 13.1865 39.5623 15.899 39.5623 21.324V28.0923Z"
                    fill="white"
                  />
                </svg>
                <h3 className="text-base font-semibold">
                  Support mail: support@credly.com
                </h3>
              </div>
            </div>

            {/* Right side forms */}
            <div className="w-full md:w-3/5 bg-white p-6 mb-8">
              {/* Buttons */}
              <div className="flex flex-col sm:flex-row items-center gap-4 p-4 bg-white rounded-lg shadow-md">
                <div className="flex flex-col sm:flex-row gap-3 flex-grow sm:justify-start">
                  {['WAEC', 'NECO', 'NYSC'].map((form) => (
                    <button
                      key={form}
                      onClick={() => setSelectedForm(form)}
                      className={`
                        px-6 py-3 rounded-lg font-medium text-sm
                        transition-all duration-200 ease-in-out
                        focus:outline-none focus:ring-2 focus:ring-offset-2
                        ${
                          selectedForm === form
                            ? 'bg-emerald-600 text-white shadow-lg hover:bg-emerald-700 focus:ring-emerald-500'
                            : 'bg-gray-100 text-gray-600 hover:bg-gray-200 hover:text-gray-700 focus:ring-gray-400'
                        }
                        transform hover:-translate-y-0.5 active:translate-y-0
                        min-w-[120px]
                      `}
                    >
                      <span className="flex items-center justify-center">
                        {form}
                        {selectedForm === form && (
                          <span className="ml-2 h-2 w-2 rounded-full bg-white" />
                        )}
                      </span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Conditional Forms */}
              {selectedForm === 'NYSC' ? (
                <FormNYSC
                  onSubmit={(event, formData) => handleSubmit(event, formData, 'NYSC')}
                  isLoading={isLoading}
                />
              ) : (
                <Form
                  onSubmit={(event, formData) => handleSubmit(event, formData, selectedForm)}
                  isLoading={isLoading}
                  subjectsList={subjectsList}
                  examTypeOptions={
                    selectedForm === 'WAEC'
                      ? WAECExamTypeOptions
                      : NECOExamTypeOptions
                  }
                  form={selectedForm}
                />
              )}
            </div>
          </div>
        </div>
      </main>

      <Modal
        isOpen={isModalOpen}
        isLoading={isLoading}
        onClose={() => setIsModalOpen(false)}
      >
        {result && <ResultComponent result={result} />}
      </Modal>

      <footer className="text-white py-4 px-4 text-center mt-8">
        <p>&copy; 2024 Credly. All rights reserved.</p>
      </footer>

      <ToastContainer />
    </div>
  );
}

export default App;
