import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";

export function ProfileForm() {
  return (
    <form className="">
      <div className="mb-4">
        <Label htmlFor="firstName">First Name</Label>
        <Input type="text" id="firstName" placeholder="" />
      </div>
      <div className="mb-4">
        <Label htmlFor="lastName">Last Name</Label>
        <Input type="text" required />
      </div>
      <div className="mb-6">
        <Label htmlFor="email">Email</Label>
        <Input disabled type="email" id="email" required />
      </div>

      <Button type="submit">Update profile</Button>
    </form>
  );
}
