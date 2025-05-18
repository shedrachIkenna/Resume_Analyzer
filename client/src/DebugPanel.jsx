import { useState } from 'react';
import { testRegistration, testValidation, checkUsers, testLogin } from './TestAuth';

function DebugPanel() {
  const [result, setResult] = useState('');

  const runTest = async (testFn) => {
    setResult('Running test...');
    try {
      const testResult = await testFn();
      setResult(testResult);
    } catch (error) {
      setResult(`Error: ${error.message}`);
    }
  };

  return (
    <div style={{ 
      margin: '20px 0',
      padding: '15px', 
      border: '1px solid #ccc',
      borderRadius: '8px',
      backgroundColor: '#242424'
    }}>
      <h3>Debug Authentication</h3>
      
      <div style={{ display: 'flex', gap: '10px', marginBottom: '15px' }}>
        <button 
          onClick={() => runTest(testRegistration)}
          style={{ padding: '8px 12px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px' }}
        >
          Test Registration
        </button>
        
        <button 
          onClick={() => runTest(testValidation)}
          style={{ padding: '8px 12px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px' }}
        >
          Test Validation
        </button>
        
        <button 
          onClick={() => runTest(checkUsers)}
          style={{ padding: '8px 12px', backgroundColor: '#17a2b8', color: 'white', border: 'none', borderRadius: '4px' }}
        >
          Check Users
        </button>
        
        <button 
          onClick={() => runTest(testLogin)}
          style={{ padding: '8px 12px', backgroundColor: '#ffc107', color: 'black', border: 'none', borderRadius: '4px' }}
        >
          Test Login
        </button>
      </div>
      
      {result && (
        <div style={{ 
          padding: '10px', 
          backgroundColor: '#242424', 
          borderRadius: '4px',
          fontFamily: 'monospace',
          whiteSpace: 'pre-wrap'
        }}>
          {result}
        </div>
      )}
    </div>
  );
}

export default DebugPanel;