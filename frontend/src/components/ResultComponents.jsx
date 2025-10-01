import React from 'react';
import PropTypes from 'prop-types';
import { toast } from 'react-toastify';
import { CheckCircle, AlertTriangle } from 'lucide-react';

// Custom Alert component
const Alert = ({ children, variant = 'default', icon: Icon }) => {
  const variantClasses = {
    default: 'bg-gray-100 border-gray-500 text-gray-700',
    success: 'bg-green-100 border-green-500 text-green-700',
    warning: 'bg-yellow-100 border-yellow-500 text-yellow-700',
    error: 'bg-red-100 border-red-500 text-red-700',
  };

  return (
    <div className={`border-l-4 p-4 ${variantClasses[variant]} flex items-start`}>
      {Icon && <Icon className="h-5 w-5 mr-3 mt-0.5" />}
      <div>{children}</div>
    </div>
  );
};

function ResultComponent({ result }) {
  const {
    mismatch = false, content = {}, mismatches = {}, success = true,
  } = result;

  if (!success) {
    toast.error(content);
    return null;
  }

  return (
    <div className="result w-full max-w-3xl mx-auto">
      <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">
        Verification Result
      </h2>
      {!mismatch && (
        <Alert variant="success" icon={CheckCircle}>
          <h3 className="font-semibold">Verified</h3>
          <p>All information has been successfully verified.</p>
        </Alert>
      )}

      {mismatch && (
        <Alert variant="warning" icon={AlertTriangle}>
          <h3 className="font-semibold">Verification Issues Detected</h3>
          <p>
            Some information do not match our records.
            Please review the highlighted discrepancies.
          </p>
        </Alert>
      )}

      {/* Render Candidate Information */}
      {content.candidate_info && (
        <div className="mb-6">
          <h3 className="text-2xl font-semibold mb-3 text-gray-800">Candidate Information</h3>
          <ul className="space-y-2 bg-white shadow rounded-lg overflow-hidden">
            {Object.entries(content.candidate_info).map(([key, value]) => {
              const hasMismatch = mismatches['Info Mismatches'] && mismatches['Info Mismatches'][key];
              return (
                <li
                  key={key}
                  className={`flex p-3 ${hasMismatch ? 'bg-red-50' : 'bg-green-50'}`}
                >
                  <span className="font-medium w-1/3 text-gray-700">{key}:</span>
                  <span className="w-2/3">
                    {hasMismatch ? (
                      <>
                        <span className="text-red-600">{mismatches['Info Mismatches'][key].received}</span>
                        <span className="text-sm block text-gray-500">
                          Expected: {mismatches['Info Mismatches'][key].expected}
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

      {/* Render Subject Grades */}
      {content.subject_grades && content.subject_grades.length > 0 && (
      <div className="mb-6">
        <h3 className="text-2xl font-semibold mb-3 text-gray-800">Subject Grades</h3>
        <ul className="grid grid-cols-2 gap-3">
          {content.subject_grades.map((subject) => {
            const hasMismatch = mismatches['Subj Mismatches'] && mismatches['Subj Mismatches'][subject.subject];
            const isNotApplicable = !!hasMismatch && mismatches['Subj Mismatches'][subject.subject].expected === 'N/A';
            return (
              <li
                key={subject.subject}
                className={`flex justify-between p-3 rounded-lg ${
                  hasMismatch ? 'bg-red-50' : 'bg-green-50'
                }`}
              >
                <span className="font-medium text-gray-700">{subject.subject}:</span>
                <span>
                  {isNotApplicable ? (
                    <span className="text-yellow-600">Not Applicable</span>
                  ) : hasMismatch ? (
                    <>
                      <span className="text-red-600">{mismatches['Subj Mismatches'][subject.subject].received}</span>
                      <span className="text-sm block text-gray-500">
                        Expected: {mismatches['Subj Mismatches'][subject.subject].expected}
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

      {/* Render Card Information */}
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
}

ResultComponent.propTypes = {
  result: PropTypes.shape({
    content: PropTypes.shape({
      candidate_info: PropTypes.objectOf(PropTypes.string),
      subject_grades: PropTypes.arrayOf(
        PropTypes.shape({
          subject: PropTypes.string.isRequired,
          grade: PropTypes.string.isRequired,
        }),
      ),
      card_info: PropTypes.objectOf(PropTypes.string),
    }),
    mismatches: PropTypes.shape({
      'Info Mismatches': PropTypes.objectOf(
        PropTypes.shape({
          expected: PropTypes.string.isRequired,
          received: PropTypes.string.isRequired,
        }),
      ),
      'Subj Mismatches': PropTypes.objectOf(
        PropTypes.shape({
          expected: PropTypes.string.isRequired,
          received: PropTypes.string.isRequired,
        }),
      ),
    }),
  }).isRequired,
};

export default ResultComponent;
