import { AboutSection } from "@/component/about-section";
import { Team } from "@/component/team";
import { Layout } from "@/component/layout";

import BackBtn from "@/atoms/back-btn";


const AboutPage = () => {
  return (
    <Layout>
      <AboutSection />
      <Team />
    </Layout>
  );
};

export default AboutPage;
