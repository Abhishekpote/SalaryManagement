"use client";

import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

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

export default function EmployeesPage() {
  const [employees, setEmployees] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingEmployee, setEditingEmployee] = useState(null);
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    job_title: "",
    country: "",
    salary: "",
    mobile_number: "",
    email: "",
    date_of_birth: "",
    date_of_joining: "",
  });

  useEffect(() => {
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    try {
      const data = await fetchAPI("/api/employees");
      setEmployees(data);
    } catch (error) {
      console.error("Failed to fetch employees:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        full_name: `${formData.first_name} ${formData.last_name}`.trim(),
        salary: parseFloat(formData.salary),
      };

      if (editingEmployee) {
        await fetchAPI(`/api/employees/${editingEmployee.id}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
      } else {
        await fetchAPI("/api/employees", {
          method: "POST",
          body: JSON.stringify(payload),
        });
      }

      setShowForm(false);
      setEditingEmployee(null);
      setFormData({
        first_name: "",
        last_name: "",
        job_title: "",
        country: "",
        salary: "",
        mobile_number: "",
        email: "",
        date_of_birth: "",
        date_of_joining: "",
      });
      fetchEmployees();
    } catch (error) {
      console.error("Failed to save employee:", error);
      alert(error.message);
    }
  };

  const handleEdit = (employee) => {
    setEditingEmployee(employee);
    setFormData({
      first_name: employee.first_name,
      last_name: employee.last_name,
      job_title: employee.job_title,
      country: employee.country,
      salary: employee.salary.toString(),
      mobile_number: employee.mobile_number,
      email: employee.email,
      date_of_birth: employee.date_of_birth ? employee.date_of_birth.split("T")[0] : "",
      date_of_joining: employee.date_of_joining ? employee.date_of_joining.split("T")[0] : "",
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (!confirm("Are you sure you want to delete this employee?")) return;
    try {
      await fetchAPI(`/api/employees/${id}`, { method: "DELETE" });
      fetchEmployees();
    } catch (error) {
      console.error("Failed to delete employee:", error);
      alert(error.message);
    }
  };

  const resetForm = () => {
    setShowForm(false);
    setEditingEmployee(null);
    setFormData({
      first_name: "",
      last_name: "",
      job_title: "",
      country: "",
      salary: "",
      mobile_number: "",
      email: "",
      date_of_birth: "",
      date_of_joining: "",
    });
  };

  if (isLoading) {
    return <div className="p-8">Loading...</div>;
  }

  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold">Manage Employees</h1>
          <p className="text-muted-foreground">View, add, edit, and delete employee records</p>
        </div>
        <Button onClick={() => { resetForm(); setShowForm(true); }}>
          Add Employee
        </Button>
      </div>

      {showForm && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>{editingEmployee ? "Edit Employee" : "Add Employee"}</CardTitle>
            <CardDescription>
              {editingEmployee ? "Update employee details" : "Enter employee details"}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="first_name">First Name</Label>
                  <Input id="first_name" name="first_name" value={formData.first_name} onChange={handleInputChange} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="last_name">Last Name</Label>
                  <Input id="last_name" name="last_name" value={formData.last_name} onChange={handleInputChange} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="job_title">Job Title</Label>
                  <Input id="job_title" name="job_title" value={formData.job_title} onChange={handleInputChange} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="country">Country</Label>
                  <Input id="country" name="country" value={formData.country} onChange={handleInputChange} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="salary">Salary</Label>
                  <Input id="salary" name="salary" type="number" step="0.01" value={formData.salary} onChange={handleInputChange} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="mobile_number">Mobile Number</Label>
                  <Input id="mobile_number" name="mobile_number" value={formData.mobile_number} onChange={handleInputChange} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input id="email" name="email" type="email" value={formData.email} onChange={handleInputChange} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="date_of_birth">Date of Birth</Label>
                  <Input id="date_of_birth" name="date_of_birth" type="date" value={formData.date_of_birth} onChange={handleInputChange} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="date_of_joining">Date of Joining</Label>
                  <Input id="date_of_joining" name="date_of_joining" type="date" value={formData.date_of_joining} onChange={handleInputChange} required />
                </div>
              </div>
              <div className="flex gap-2">
                <Button type="submit">{editingEmployee ? "Update" : "Add"}</Button>
                <Button type="button" variant="outline" onClick={resetForm}>Cancel</Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Employee List</CardTitle>
          <CardDescription>Total: {employees.length} employees</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left p-3">Name</th>
                  <th className="text-left p-3">Job Title</th>
                  <th className="text-left p-3">Country</th>
                  <th className="text-left p-3">Salary</th>
                  <th className="text-left p-3">Mobile</th>
                  <th className="text-left p-3">Email</th>
                  <th className="text-left p-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                {employees.length === 0 ? (
                  <tr>
                    <td colSpan="7" className="text-center p-4 text-muted-foreground">No employees found</td>
                  </tr>
                ) : (
                  employees.map((emp) => (
                    <tr key={emp.id} className="border-b hover:bg-muted/50">
                      <td className="p-3">{emp.full_name}</td>
                      <td className="p-3">{emp.job_title}</td>
                      <td className="p-3">{emp.country}</td>
                      <td className="p-3">${emp.salary?.toLocaleString()}</td>
                      <td className="p-3">{emp.mobile_number}</td>
                      <td className="p-3">{emp.email}</td>
                      <td className="p-3">
                        <div className="flex gap-2">
                          <Button size="sm" variant="outline" onClick={() => handleEdit(emp)}>Edit</Button>
                          <Button size="sm" variant="destructive" onClick={() => handleDelete(emp.id)}>Delete</Button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}