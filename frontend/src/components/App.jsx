import React, { useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Modal from './Modal';
import ResultComponents from './ResultComponents'; // singular fix
import Form from './Form';
import FormNYSC from './FormNYSC';

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

  // Submission handler
  const handleSubmit = async (event, formData, formType) => {
    event.preventDefault();
    setResult(null);
    setIsLoading(true);

    let url = '';
    if (formType === 'WAEC') {
      url = 'http://127.0.0.1:5000/api/waec';
    } else if (formType === 'NECO') {
      url = 'http://127.0.0.1:5000/api/neco';
    } else if (formType === 'NYSC') {
      url = 'http://127.0.0.1:5000/api/nysc';
    }

    try {
      const resp = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      const data = await resp.json();
      if (!resp.ok && resp.status !== 422) {
        toast.error(data.error || data.message || 'Verification service error');
      } else {
        setResult(data);
        setIsModalOpen(true);
      }
    } catch (err) {
      toast.error('Verification failed. Please ensure backend server is running.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-emerald-800">
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="flex flex-col md:flex-row">
            <div className="w-full md:w-2/5 bg-emerald-800 text-white p-8">
              <h2 className="text-3xl font-bold mb-6">CREDLY RESULTS</h2>
              <h3 className="text-xl font-semibold mb-4">How it works:</h3>
              <ul className="list-disc list-inside space-y-2">
                <li>Choose WAEC, NECO, or NYSC verification.</li>
                <li>Fill in the required details in the form.</li>
                <li>Click the &ldquo;Verify&rdquo; button.</li>
                <li>View detailed verification and any mismatches.</li>
              </ul>
              <div className="mt-8 flex items-center space-x-4">
                <h3 className="text-base font-semibold">Support: support@credly.com</h3>
              </div>
            </div>

            <div className="w-full md:w-3/5 bg-white p-6 mb-8">
              <div className="flex flex-col sm:flex-row items-center gap-4 p-4 bg-white rounded-lg shadow-md">
                <div className="flex-shrink-0">
                  <img
                    src={`images/${selectedForm}.png`}
                    alt={`${selectedForm} logo`}
                    className="h-16 w-auto"
                  />
                </div>

                <div className="flex flex-col sm:flex-row gap-3 flex-grow sm:justify-start">
                  <button
                    type="button"
                    onClick={() => setSelectedForm('WAEC')}
                    className={
                      selectedForm === 'WAEC'
                        ? 'px-6 py-3 bg-emerald-600 text-white rounded-lg'
                        : 'px-6 py-3 bg-gray-100 rounded-lg'
                    }
                  >
                    WAEC
                  </button>
                  <button
                    type="button"
                    onClick={() => setSelectedForm('NECO')}
                    className={
                      selectedForm === 'NECO'
                        ? 'px-6 py-3 bg-emerald-600 text-white rounded-lg'
                        : 'px-6 py-3 bg-gray-100 rounded-lg'
                    }
                  >
                    NECO
                  </button>
                  <button
                    type="button"
                    onClick={() => setSelectedForm('NYSC')}
                    className={
                      selectedForm === 'NYSC'
                        ? 'px-6 py-3 bg-emerald-600 text-white rounded-lg'
                        : 'px-6 py-3 bg-gray-100 rounded-lg'
                    }
                  >
                    NYSC
                  </button>
                </div>
              </div>

              {selectedForm === 'NYSC' ? (
                <FormNYSC
                  onSubmit={(e, fd) => handleSubmit(e, fd, 'NYSC')}
                  isLoading={isLoading}
                />
              ) : (
                <Form
                  onSubmit={(e, fd) => handleSubmit(e, fd, selectedForm)}
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
        {result && <ResultComponents result={result} />}
      </Modal>

      <footer className="text-white py-4 px-4 text-center mt-8">
        <p>&copy; 2025 Credly. All rights reserved.</p>
      </footer>

      <ToastContainer position="top-right" />
    </div>
  );
}

export default App;
