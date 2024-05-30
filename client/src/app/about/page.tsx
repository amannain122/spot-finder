import { Header } from "@/component/header";
import { AboutSection } from "@/component/about-section";
import { Team } from "@/component/team";

const AboutPage = () => {
  return (
    <div className="p-width m-4 relative">
      <Header />
      <AboutSection />
      <Team />
    </div>
  );
};

export default AboutPage;
