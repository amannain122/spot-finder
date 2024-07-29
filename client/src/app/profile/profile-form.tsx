"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { getUser, handleError, updateUser } from "@/lib/server";
import { useToast } from "@/components/ui/use-toast";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";

const checkField = (data: any) => {
  if (!data.first_name) {
    return { isValid: false, message: "Please enter first name!" };
  }
  if (!data.last_name) {
    return { isValid: false, message: "Please enter last name!" };
  }
  return { isValid: true, message: "" };
};

export function ProfileForm() {
  const { toast } = useToast();
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState({
    first_name: "",
    last_name: "",
    email: "",
  });

  const handleUpdate = async (e: any) => {
    e?.preventDefault();
    const { isValid, message } = checkField(data);
    if (!isValid) {
      return toast({ title: message || "Something is wrong 🤔" });
    }
    setLoading(true);
    const response = await updateUser({
      first_name: data.first_name || "",
      last_name: data.last_name || "",
    });
    if (response.status === "success") {
      toast({
        title: "Profile Updated",
      });
    } else {
      const error = handleError(response.data);
      toast({ title: error || "Something went wrong" });
    }
    setLoading(false);
  };

  useEffect(() => {
    const getProfile = async () => {
      const response = await getUser();
      if (response.status === "success") {
        console.log(response.data);
        setData({
          first_name: response?.data?.first_name || "",
          last_name: response?.data?.last_name || "",
          email: response?.data?.email || "",
        });
      }
    };
    getProfile();
  }, []);

  return (
    <form className="">
      <div className="mb-4">
        <Label htmlFor="firstName">
          First Name<span className="text-red-500">*</span>
        </Label>
        <Input
          type="text"
          id="firstName"
          placeholder=""
          value={data.first_name}
          onChange={(e) => setData({ ...data, first_name: e.target.value })}
        />
      </div>
      <div className="mb-4">
        <Label htmlFor="lastName">
          Last Name<span className="text-red-500">*</span>
        </Label>
        <Input
          type="text"
          required
          value={data.last_name}
          onChange={(e) => setData({ ...data, last_name: e.target.value })}
        />
      </div>
      <div className="mb-6">
        <Label htmlFor="email">Email</Label>
        <Input disabled type="email" id="email" required value={data.email} />
      </div>
      <Button
        aria-label="Update profile"
        aria-live="polite"
        type="submit"
        onClick={(e) => handleUpdate(e)}
        disabled={loading}
      >
        {loading ? "Updating..." : "Update Profile"}
      </Button>
    </form>
  );
}
