const API_BASE_URL = '/api';

const Alert = ({ message, type }) => {
    const bgColor = type === 'error' ? 'bg-red-100' : type === 'success' ? 'bg-green-100' : 'bg-yellow-100';
    const textColor = type === 'error' ? 'text-red-700' : type === 'success' ? 'text-green-700' : 'text-yellow-700';
    const borderColor = type === 'error' ? 'border-red-400' : type === 'success' ? 'border-green-400' : 'border-yellow-400';

    return (
        <div className={`p-4 mb-4 ${bgColor} ${textColor} ${borderColor} border-l-4 rounded-r-xl`} role="alert">
            <p className="font-bold">
                {type === 'error' ? 'Error' : type === 'success' ? 'Success' : 'Info'}
            </p>
            <p>{message}</p>
        </div>
    );
};

const Button = ({ onClick, children, color = 'indigo' }) => {
    const baseClasses = "w-full py-2 px-4 rounded-md font-medium text-white transition duration-150 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-offset-2";
    const colorClasses = {
        indigo: "bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500",
        teal: "bg-teal-600 hover:bg-teal-700 focus:ring-teal-500",
    };

    return (
        <button
            onClick={onClick}
            className={`${baseClasses} ${colorClasses[color]}`}
        >
            {children}
        </button>
    );
};

const CTFChallenge = () => {
    const [username, setUsername] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [newUsername, setNewUsername] = React.useState('');
    const [newPassword, setNewPassword] = React.useState('');
    const [token, setToken] = React.useState('');
    const [alertMessage, setAlertMessage] = React.useState('');
    const [alertType, setAlertType] = React.useState('');
    const alertTimerRef = React.useRef(null);

    const showAlert = (message, type) => {
        if (alertTimerRef.current) {
            clearTimeout(alertTimerRef.current);
        }

        setAlertMessage(message);
        setAlertType(type);

        alertTimerRef.current = setTimeout(() => {
            setAlertMessage('');
            setAlertType('');
            alertTimerRef.current = null;
        }, 5000);
    };

    const login = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`${API_BASE_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });
            const data = await response.json();
            if (response.ok) {
                setToken(data.access_token);
                setNewUsername(username);
                showAlert('Login successful', 'success');
            } else {
                throw new Error(data.detail || 'Login failed');
            }
        } catch (err) {
            showAlert(err.message, 'error');
        }
    };

    const updateUser = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`${API_BASE_URL}/update_user`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({ username: newUsername, password: newPassword }),
            });
            const data = await response.json();
            if (response.ok) {
                setToken(data.new_token);
                showAlert('User information updated successfully', 'success');
            } else {
                throw new Error(data.detail || 'Update failed');
            }
        } catch (err) {
            showAlert(err.message, 'error');
        }
    };

    const getFlag = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/get_flag`, {
                headers: { 'Authorization': `Bearer ${token}` },
            });
            const data = await response.json();
            if (response.ok) {
                showAlert(`Flag: ${data.flag}`, 'success');
            } else {
                throw new Error(data.detail || 'Failed to get flag');
            }
        } catch (err) {
            showAlert(err.message, 'error');
        }
    };

    return (
        <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-xl">
            <h1 className="text-2xl font-bold mb-6 text-center text-gray-800">SVUCTF Challenge</h1>

            {alertMessage && <Alert message={alertMessage} type={alertType} />}

            {!token ? (
                <form onSubmit={login} className="mb-4 space-y-4">
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    />
                    <Button type="submit" color="indigo">Login</Button>
                </form>
            ) : (
                <div className="space-y-4">
                    <form onSubmit={updateUser} className="space-y-4">
                        <input
                            type="text"
                            placeholder="New Username"
                            value={newUsername}
                            onChange={(e) => setNewUsername(e.target.value)}
                            className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                        />
                        <input
                            type="password"
                            placeholder="New Password"
                            value={newPassword}
                            onChange={(e) => setNewPassword(e.target.value)}
                            className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                        />
                        <Button type="submit" color="teal">Update User Info</Button>
                    </form>

                    <Button onClick={getFlag} color="teal">Get Flag</Button>
                </div>
            )}
        </div>
    );
};

ReactDOM.render(<CTFChallenge />, document.getElementById('root'));

