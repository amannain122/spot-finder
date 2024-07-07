"use client";
import React, { useState } from "react";
import moment from "moment";
import { useRouter } from "next/navigation";
import { handleError, login, register, setJwtToken } from "@/lib/server";
import { useToast } from "@/components/ui/use-toast";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export const LoginForm = () => {
  const { toast } = useToast();
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e: any) => {
    e?.preventDefault();
    setLoading(true);
    if (!email) return toast({ title: "Please enter your email" });
    if (!password) return toast({ title: "Please enter your password" });
    const response = await login({ email: email, password: password });
    if (response.status === "success") {
      setJwtToken(response?.data?.access || "");
      const formattedDate = moment().format("dddd, MMMM D, YYYY [at] h:mm A");
      toast({
        title: "Login Successfull!!",
        description: formattedDate || "",
      });
      router.push("/");
    } else {
      const error = handleError(response.data);
      toast({ title: error || "Something went wrong" });
    }
    setLoading(false);
  };
  return (
    <>
      <form>
        <div className="mb-6">
          <Label htmlFor="email">Email</Label>
          <Input
            type="email"
            id="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="mb-6">
          <Label htmlFor="password">Password</Label>
          <Input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <Button
          className="w-full"
          type="submit"
          disabled={loading}
          onClick={(e) => handleLogin(e)}
        >
          {loading ? "Login..." : "Login"}
        </Button>
      </form>
    </>
  );
};

const checkField = (data: any) => {
  if (!data.first_name) {
    return { isValid: false, message: "Please enter first name!" };
  }
  if (!data.last_name) {
    return { isValid: false, message: "Please enter last name!" };
  }
  if (!data.email) {
    return { isValid: false, message: "Please enter email!" };
  }
  if (!data.password) {
    return { isValid: false, message: "Please enter password!" };
  }
  return { isValid: true, message: "" };
};

export const RegisterForm = () => {
  const { toast } = useToast();
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
  });

  const handleRegister = async (e: any) => {
    e?.preventDefault();
    const { isValid, message } = checkField(data);
    if (!isValid) {
      return toast({ title: message || "Something is wrong 🤔" });
    }
    setLoading(true);
    const response = await register(data);
    if (response.status === "success") {
      toast({
        title: "Registration Successfull!!",
      });
      router.push("/login");
    } else {
      const error = handleError(response.data);
      toast({ title: error || "Something went wrong" });
    }
    setLoading(false);
  };

  return (
    <>
      <form>
        <div className="mb-4">
          <Label htmlFor="firstName">First Name</Label>
          <Input
            type="text"
            id="firstName"
            placeholder=""
            value={data.first_name}
            onChange={(e) => setData({ ...data, first_name: e.target.value })}
          />
        </div>
        <div className="mb-4">
          <Label htmlFor="lastName">Last Name</Label>
          <Input
            type="text"
            required
            value={data.last_name}
            onChange={(e) => setData({ ...data, last_name: e.target.value })}
          />
        </div>
        <div className="mb-6">
          <Label htmlFor="email">Email</Label>
          <Input
            type="email"
            id="email"
            required
            value={data.email}
            onChange={(e) => setData({ ...data, email: e.target.value })}
          />
        </div>
        <div className="mb-6">
          <Label htmlFor="password">Password</Label>
          <Input
            type="password"
            required
            value={data.password}
            onChange={(e) => setData({ ...data, password: e.target.value })}
          />
        </div>
        <Button
          className="w-full"
          type="submit"
          disabled={loading}
          onClick={(e) => handleRegister(e)}
        >
          {loading ? "Creating..." : "Create Account"}
        </Button>
      </form>
    </>
  );
};
