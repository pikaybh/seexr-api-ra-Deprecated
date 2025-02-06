import { useAuthStore } from '@/store/auth';


export function requireAuth(location) {
    const auth = useAuthStore();

    if (!auth.isAuthenticated) {
        alert("로그인이 필요합니다.");
        location.$router.push("/login");
    }
}
