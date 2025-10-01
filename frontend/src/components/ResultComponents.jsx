// frontend/src/components/ResultComponents.jsx
import React from 'react';
import PropTypes from 'prop-types';
import { toast } from 'react-toastify';
import { CheckCircle, AlertTriangle, XCircle } from 'lucide-react';

// Simple Alert UI used in the component
const Alert = ({ children, variant = 'default', Icon }) => {
  const variantClasses = {
    default: 'bg-gray-100 border-gray-400 text-gray-700',
    success: 'bg-green-100 border-green-500 text-green-700',
    warning: 'bg-yellow-100 border-yellow-500 text-yellow-700',
    error: 'bg-red-100 border-red-500 text-red-700',
  };

  return (
    <div className={`border-l-4 p-4 ${variantClasses[variant]} flex items-start rounded-md mb-4`}>
      {Icon && <Icon className="h-5 w-5 mr-3 mt-0.5 flex-shrink-0" />}
      <div className="flex-1">{children}</div>
    </div>
  );
};

Alert.propTypes = {
  children: PropTypes.node.isRequired,
  variant: PropTypes.oneOf(['default', 'success', 'warning', 'error']),
  Icon: PropTypes.func,
};

Alert.defaultProps = {
  variant: 'default',
  Icon: null,
};

const ResultComponents = ({ result }) => {
  if (!result) {
    return <p className="text-gray-500 text-center">No result to display yet.</p>;
  }

  const {
    success = true,
    mismatch = false,
    content = {},
    mismatches = {},
    message,
    error,
  } = result;

  if (!success) {
    // show toast and render a friendly error box
    toast.error(message || error || 'Verification failed');
    return (
      <Alert variant="error" Icon={XCircle}>
        <h3 className="font-semibold">Verification Failed</h3>
        <p>{message || error || 'An unknown error occurred.'}</p>
      </Alert>
    );
  }

  return (
    <div className="result w-full max-w-3xl mx-auto">
      <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">Verification Result</h2>

      {!mismatch && (
        <Alert variant="success" Icon={CheckCircle}>
          <h3 className="font-semibold">Verified</h3>
          <p>All information has been successfully verified ✅</p>
        </Alert>
      )}

      {mismatch && (
        <Alert variant="warning" Icon={AlertTriangle}>
          <h3 className="font-semibold">Verification Issues Detected</h3>
          <p>Some information does not match our records. Please review discrepancies below.</p>
        </Alert>
      )}

      {/* Candidate Information */}
      {content.candidate_info && (
        <div className="mb-6">
          <h3 className="text-2xl font-semibold mb-3 text-gray-800">Candidate Information</h3>
          <ul className="space-y-2 bg-white shadow rounded-lg overflow-hidden">
            {Object.entries(content.candidate_info).map(([key, value]) => {
              const mismatchInfo = mismatches && mismatches['Info Mismatches'] && mismatches['Info Mismatches'][key];
              return (
                <li
                  key={key}
                  className={`flex p-3 ${mismatchInfo ? 'bg-red-50' : 'bg-green-50'}`}
                >
                  <span className="font-medium w-1/3 text-gray-700">{key}:</span>
                  <span className="w-2/3">
                    {mismatchInfo ? (
                      <>
                        <span className="text-red-600">{mismatchInfo.received}</span>
                        <span className="text-sm block text-gray-500">
                          Expected: {mismatchInfo.expected}
                        </span>
                      </>
                    ) : (
                      <span className="text-green-600">{value}</span>
                    )}
                  </span>
                </li>
              );
            })}
          </ul>
        </div>
      )}

      {/* Subject Grades */}
      {Array.isArray(content.subject_grades) && content.subject_grades.length > 0 && (
        <div className="mb-6">
          <h3 className="text-2xl font-semibold mb-3 text-gray-800">Subject Grades</h3>
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {content.subject_grades.map((subject) => {
              const mismatchSubj = mismatches && mismatches['Subj Mismatches'] && mismatches['Subj Mismatches'][subject.subject];
              const isNA = mismatchSubj && mismatchSubj.expected === 'N/A';
              return (
                <li
                  key={subject.subject}
                  className={`flex justify-between p-3 rounded-lg ${
                    mismatchSubj ? 'bg-red-50' : 'bg-green-50'
                  }`}
                >
                  <span className="font-medium text-gray-700">{subject.subject}:</span>
                  <span>
                    {isNA ? (
                      <span className="text-yellow-600">Not Applicable</span>
                    ) : mismatchSubj ? (
                      <>
                        <span className="text-red-600">{mismatchSubj.received}</span>
                        <span className="text-sm block text-gray-500">
                          Expected: {mismatchSubj.expected}
                        </span>
                      </>
                    ) : (
                      <span className="text-green-600">{subject.grade}</span>
                    )}
                  </span>
                </li>
              );
            })}
          </ul>
        </div>
      )}

      {/* Card Information */}
      {content.card_info && (
        <div className="mb-6">
          <h3 className="text-2xl font-semibold mb-3 text-gray-800">Card Information</h3>
          <ul className="space-y-2 bg-white shadow rounded-lg overflow-hidden">
            {Object.entries(content.card_info).map(([key, value]) => (
              <li key={key} className="flex p-3 bg-blue-50">
                <span className="font-medium w-1/3 text-gray-700">{key}:</span>
                <span className="w-2/3 text-blue-600">{value}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

ResultComponents.propTypes = {
  result: PropTypes.shape({
    success: PropTypes.bool,
    mismatch: PropTypes.bool,
    message: PropTypes.string,
    error: PropTypes.string,
    content: PropTypes.shape({
      candidate_info: PropTypes.objectOf(PropTypes.oneOfType([PropTypes.string, PropTypes.number])),
      subject_grades: PropTypes.arrayOf(
        PropTypes.shape({
          subject: PropTypes.string.isRequired,
          grade: PropTypes.string.isRequired,
        }),
      ),
      card_info: PropTypes.objectOf(PropTypes.oneOfType([PropTypes.string, PropTypes.number])),
    }),
    mismatches: PropTypes.shape({
      'Info Mismatches': PropTypes.objectOf(
        PropTypes.shape({
          expected: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
          received: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
        }),
      ),
      'Subj Mismatches': PropTypes.objectOf(
        PropTypes.shape({
          expected: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
          received: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
        }),
      ),
    }),
  }),
};

ResultComponents.defaultProps = {
  result: null,
};

export default ResultComponents;
