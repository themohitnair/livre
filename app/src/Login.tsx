import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { Input } from "./components/ui/input";
import { Button } from "./components/ui/button";
import { useState } from "react";
import { login } from './auth';

const Login = () => {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [message, setMessage] = useState<string>("");

  const handleLogin = async () => {
    try {
      const { access_token } = await login(username, password);
      setMessage("Login successful!");
      // You can store the token in localStorage or state for further API requests
      localStorage.setItem('access_token', access_token);
    } catch (error: unknown) {
      if (error instanceof Error) {
        setMessage("Login failed: " + error.message);
      } else {
        setMessage("An unknown error occurred.");
      }
    }
  };

  return (    
    <div className="flex justify-center items-center h-screen">
      <Card className="w-3/12">
        <CardHeader className="flex items-center justify-center">
          <CardTitle>Login</CardTitle>
        </CardHeader>
        <CardContent>
          <Input
            placeholder="Username"
            className="mb-3"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {message && (
            <div className="mt-3 text-center text-red-500">{message}</div>
          )}
        </CardContent>
        <CardFooter className="w-full">
          <Button
            variant="default"
            className="w-full"
            onClick={handleLogin}
          >
            Login
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default Login;