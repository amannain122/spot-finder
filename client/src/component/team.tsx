"use client";

import { useState, useEffect } from "react";
import axios from "axios";

const people = [
  {
    name: "Leandro Sartini De Campos",
    role: "Leader",
    username: "leandro-sartini",
  },
  {
    name: "Jorge Rodrigo Velazquez Espinosa",
    role: "Co-Leader",
    username: "RooVelazquez",
  },
  {
    name: "Saraka Don",
    role: "Co-Machine Learning Engineer",
    username: "sahaswin",
  },
  {
    name: "Gurbachan Singh",
    role: "Data Analyst - Dashboard Specialist",
    username: "",
  },
  {
    name: "Ogechi Tina Ukanwune",
    role: "Data Analyst - Insights Specialist",
    username: "",
  },
  {
    name: "Bibek Ranjit",
    role: "Cloud Architect",
    username: "drummersoul",
  },
  {
    name: "Prakash Pun",
    role: "Frontend Developer",
    username: "prakash-pun",
  },
  {
    name: "Aman Nain",
    role: "Data Engineer",
    username: "amannain122",
  },
  {
    name: "Anjitha Mohan",
    role: "Backend Developer",
    username: "anjithamohan",
  },
  {
    name: "Jissy Jayaprakash",
    role: "DevOps Engineer",
    username: "Jissy96",
  },
  {
    name: "Jisna D Kunju",
    role: "UI/UX Specialist",
    username: "",
  },
];

export const TeamAvatar = ({ username }: { username: string }) => {
  const [image, setImage] = useState(
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
  );
  // https://api.github.com/users/prakash-pun
  const [, setLoading] = useState(true);

  useEffect(() => {
    const fetchAvatar = async () => {
      try {
        setLoading(true);
        if (!username) {
          setLoading(false);
          return;
        }
        const response = await axios.get(
          `https://api.github.com/users/${username}`
        );
        if (response) {
          setImage(response.data.avatar_url);
        } else {
          setImage(
            "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
          );
        }
      } catch (err) {
        setLoading(false);
      }
    };

    fetchAvatar();
  }, [username]);

  return (
    <a href={`https://github.com/${username}`} target="_blank">
      <img
        className="h-16 w-16 rounded-full"
        src={image}
        loading="lazy"
        alt={`${username} avatar`}
      />
    </a>
  );
};

export const Team = () => {
  return (
    <div className="py-10 sm:py-8">
      <div className="mx-auto grid max-w-7xl gap-x-8 gap-y-20 px-6 lg:px-8 xl:grid-cols-3">
        <div className="max-w-2xl">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Meet our Team
          </h2>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quasi in,
            ad saepe consequatur vero voluptate odit, asperiores quaerat vel
            molestias quod illo quos. Totam cupiditate reiciendis sunt rerum rem
            laudantium!
          </p>
        </div>
        <ul
          role="list"
          className="grid gap-x-8 gap-y-12 sm:grid-cols-2 sm:gap-y-16 xl:col-span-2"
        >
          {people.map((person) => (
            <li key={person.name}>
              <div className="flex items-center gap-x-6">
                <TeamAvatar username={person?.username || ""} />
                <div>
                  <h3 className="text-base font-semibold leading-7 tracking-tight text-gray-900">
                    {person.name}
                  </h3>
                  <p className="text-sm font-semibold leading-6 text-indigo-600">
                    {person.role}
                  </p>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
