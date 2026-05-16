"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/hooks/useAuth";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";

const API_BASE_URL = "http://localhost:5000";

async function fetchAPI(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const config = {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    credentials: "include",
  };
  const response = await fetch(url, config);
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }
  return response.json();
}

export default function Home() {
  const { user, logout } = useAuth();
  const [countryStats, setCountryStats] = useState({});
  const [jobInsight, setJobInsight] = useState(null);
  const [selectedCountry, setSelectedCountry] = useState("");
  const [jobTitle, setJobTitle] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [jobTitles, setJobTitles] = useState([]);

  useEffect(() => {
    fetchCountryStats();
    fetchJobTitles();
  }, []);

  const fetchCountryStats = async () => {
    try {
      const data = await fetchAPI("/api/employees/insights/by-country");
      setCountryStats(data);
    } catch (error) {
      console.error("Failed to fetch country stats:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchJobTitles = async () => {
    try {
      const data = await fetchAPI("/api/employees/job-titles");
      setJobTitles(data);
    } catch (error) {
      console.error("Failed to fetch job titles:", error);
    }
  };

  const fetchJobInsight = async () => {
    if (!selectedCountry || !jobTitle) return;
    try {
      const data = await fetchAPI(
        `/api/employees/insights/by-country-job?country=${encodeURIComponent(selectedCountry)}&job_title=${encodeURIComponent(jobTitle)}`
      );
      setJobInsight(data);
    } catch (error) {
      console.error("Failed to fetch job insight:", error);
      setJobInsight({ message: "No data found" });
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    setIsSearching(true);
    try {
      const data = await fetchAPI(`/api/employees/search?q=${encodeURIComponent(searchQuery)}`);
      setSearchResults(data);
    } catch (error) {
      console.error("Failed to search employees:", error);
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  const countries = Object.keys(countryStats);

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900 p-8">
      <div className="max-w-5xl mx-auto space-y-8">
        <div className="flex items-center justify-between">
          <div className="text-center">
            <h1 className="text-4xl font-bold tracking-tight">Salary Management</h1>
            <p className="text-muted-foreground">Manage your team&apos;s compensation with ease</p>
          </div>
          
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Salary Insights by Country</CardTitle>
            <CardDescription>Minimum, Maximum, and Average salary per country</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <p>Loading...</p>
            ) : countries.length === 0 ? (
              <p className="text-muted-foreground">No employee data available</p>
            ) : (
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {countries.map((country) => (
                  <Card key={country} className="bg-slate-50 dark:bg-slate-800">
                    <CardHeader className="pb-2">
                      <CardTitle className="text-lg">{country}</CardTitle>
                      <CardDescription>{countryStats[country].employee_count} employees</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm text-muted-foreground">Min</span>
                          <span className="text-sm font-medium">${countryStats[country].min_salary.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-muted-foreground">Max</span>
                          <span className="text-sm font-medium">${countryStats[country].max_salary.toLocaleString()}</span>
                        </div>
                        <Separator />
                        <div className="flex justify-between">
                          <span className="text-sm font-medium">Average</span>
                          <span className="text-sm font-bold text-green-600">${countryStats[country].avg_salary.toLocaleString()}</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Job Title Salary Insight</CardTitle>
            <CardDescription>Average salary for a specific job title in a country</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex gap-4 mb-4">
              <div className="flex-1 space-y-2">
                <Label htmlFor="country">Country</Label>
                <select
                  id="country"
                  className="w-full h-10 px-3 border rounded-md bg-background"
                  value={selectedCountry}
                  onChange={(e) => setSelectedCountry(e.target.value)}
                >
                  <option value="">Select country</option>
                  {countries.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>
              <div className="flex-1 space-y-2">
                <Label htmlFor="jobTitle">Job Title</Label>
                <select
                  id="jobTitle"
                  className="w-full h-10 px-3 border rounded-md bg-background"
                  value={jobTitle}
                  onChange={(e) => setJobTitle(e.target.value)}
                >
                  <option value="">Select job title</option>
                  {jobTitles.map((jt) => (
                    <option key={jt} value={jt}>{jt}</option>
                  ))}
                </select>
              </div>
              <div className="flex items-end">
                <Button onClick={fetchJobInsight} disabled={!selectedCountry || !jobTitle}>
                  Get Insight
                </Button>
              </div>
            </div>

            {jobInsight && (
              <div className="mt-4 p-4 bg-slate-100 dark:bg-slate-800 rounded-lg">
                {"message" in jobInsight ? (
                  <p className="text-muted-foreground">{jobInsight.message}</p>
                ) : (
                  <div className="grid gap-2 md:grid-cols-4">
                    <div className="text-center">
                      <p className="text-sm text-muted-foreground">Country</p>
                      <p className="font-medium">{jobInsight.country}</p>
                    </div>
                    <div className="text-center">
                      <p className="text-sm text-muted-foreground">Job Title</p>
                      <p className="font-medium">{jobInsight.job_title}</p>
                    </div>
                    <div className="text-center">
                      <p className="text-sm text-muted-foreground">Employees</p>
                      <p className="font-medium">{jobInsight.employee_count}</p>
                    </div>
                    <div className="text-center">
                      <p className="text-sm text-muted-foreground">Avg Salary</p>
                      <p className="font-bold text-green-600">${jobInsight.avg_salary.toLocaleString()}</p>
                    </div>
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Search Employee</CardTitle>
            <CardDescription>Find an employee by name or email</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex gap-2">
              <div className="flex-1 space-y-2">
                <Label htmlFor="search">Search</Label>
                <Input
                  id="search"
                  placeholder="Enter name or email..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                />
              </div>
              <div className="flex items-end">
                <Button onClick={handleSearch} disabled={isSearching}>
                  {isSearching ? "Searching..." : "Search"}
                </Button>
              </div>
            </div>

            {searchResults.length > 0 && (
              <div className="mt-4">
                <p className="text-sm font-medium mb-2">Found {searchResults.length} employee(s):</p>
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {searchResults.map((emp) => (
                    <div key={emp.id} className="flex items-center justify-between p-3 bg-slate-100 dark:bg-slate-800 rounded-lg">
                      <div>
                        <p className="font-medium">{emp.full_name}</p>
                        <p className="text-sm text-muted-foreground">
                          {emp.job_title} - {emp.country}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="font-medium">${emp.salary.toLocaleString()}</p>
                        <p className="text-sm text-muted-foreground">ID: {emp.id}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {searchQuery && searchResults.length === 0 && !isSearching && (
              <p className="text-muted-foreground mt-4">No employees found matching "{searchQuery}"</p>
            )}
          </CardContent>
        </Card>
      </div>
    </main>
  );
}